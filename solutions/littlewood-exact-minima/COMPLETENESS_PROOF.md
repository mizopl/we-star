# Completeness, Symmetry, and IEEE-754 Soundness Proof (`Engine 3` / `Engine 4 v4.2`)

> **Scope & `-0 Hype` Limitations First:**
> This document provides a self-contained mathematical proof that our exact $d = 2$ Cooley-Tukey Phase-Projection Meet-in-the-Middle (MITM) certifier ([`engine4_cuda_mitm.cu`](engine4_cuda_mitm.cu), `v4.2` hardened after independent blind `S-1` audit, and CPU twin [`engine3_bitset_mitm.py`](engine3_bitset_mitm.py)) has **zero false rejections** across the entire $2^N$ Littlewood polynomial search space $\{-1, +1\}^N$ for every $N \in [4, 64]$ ($n = N - 1 \in [3, 63]$).
>
> **Explicit Limitations:**
> 1. **Finite-$N$ exact optimal value bracket only:** Certifying exact global minimum value brackets for $M_n$ and $C^+$ at finite $n \le 55$ ($N \le 56$) does **not** decide asymptotic behavior as $n \to \infty$ (where OpenAI + el Abdalaoui `arXiv:2610.30797` resolved Erdős Problem #1150 negatively via a Lean-verified proof that $\max|P_n| \le (1 + \eta)\sqrt{N}$ exists for sufficiently large $N$; see [`FRONTIER_RECON_2018_2026.md`](FRONTIER_RECON_2018_2026.md)). Uniqueness of the optimal orbit within the $10^{-4}$ squared-norm window is not claimed.
> 2. **Trust boundary:** Soundness relies on IEEE-754 `binary64` with FMA compliance of host `libm` and CUDA `nvcc -O3 -std=c++17` (strictly **without** `--use_fast_math`), plus standard hardware correctness (no silent bit-flips on ECC A100 VRAM). Every dimension $N \ge 53$ is independently cross-checked on **two distinct grids** ($G = 256$ and $G = 128$), and Stage-1 survivor SHA-256 digests are cross-audited independently on CPU (`verify_dual_lb.py` / standalone C checker, eliminating single-binary GPU trust).

---

## 1. Problem Definition & Dual Normalizations

Let $g(z) = \sum_{j=0}^{N-1} c_j z^j$ with $c_j \in \{-1, +1\}$ (degree $n = N - 1$, $N$ coefficients), and let
$$f(\theta) := |g(e^{i\theta})|^2 = N + 2 \sum_{k=1}^{N-1} R_k \cos(k\theta), \qquad R_k = \sum_{j=0}^{N-1-k} c_j c_{j+k} \in \mathbb{Z}.$$
Define the exact global minimum squared supremum:
$$M^*(N) := \min_{c \in \{-1,+1\}^N} \sup_{\theta \in [0, 2\pi)} |g_c(e^{i\theta})|^2.$$

All results report **both** standard literature normalizations side-by-side:
1. **Classical Odlyzko / Tao / Erdős RMS normalization ($M_n \equiv C_{\text{rms}}$):**
   $$M_n := \frac{\sqrt{M^*(N)}}{\sqrt{N}} = \frac{\min_{c \in \{-1,+1\}^{n+1}} \sup_{|z|=1} |P_n(z)|}{\sqrt{n + 1}}, \qquad N = n + 1.$$
2. **EinsteinArena / AlphaEvolve V2 normalization ($C^+$):**
   $$C^+(N) := \frac{\sqrt{M^*(N)}}{\sqrt{N + 1}} = M_n \sqrt{\frac{N}{N + 1}}.$$

A certificate for dimension $N$ exhibits:
- A concrete binary witness $c^* \in \{-1, +1\}^N$ with rigorous continuous bracket $f_{\text{lo}}(c^*) \le \sup_{|z|=1} |g_{c^*}(z)|^2 \le f_{\text{ub}}(c^*)$, and
- A target threshold $M_{\text{target}} = f_{\text{lo}}(c^*) - 10^{-4}$ together with an exhaustive proof that **no** $c \in \{-1, +1\}^N$ satisfies $\sup_{|z|=1} |g_c(z)|^2 \le M_{\text{target}}$, yielding the exact interval
  $$\sqrt{M_{\text{target}} / N} < M_n \le \sqrt{f_{\text{ub}}(c^*) / N} \qquad (\text{gap} \le 2 \times 10^{-6}).$$

---

## 2. Exact $d = 2$ Polyphase Decomposition & Complete $D_4$ Symmetry Quotient

Decompose any $g(z) = \sum_{j=0}^{N-1} c_j z^j$ into its even and odd polyphase halves:
$$g(z) = g_e(z^2) + z\, g_o(z^2), \qquad M_e = \lceil N / 2 \rceil,\; M_o = \lfloor N / 2 \rfloor,$$
where $g_e[m] = c_{2m}$ ($0 \le m < M_e$) and $g_o[m] = c_{2m+1}$ ($0 \le m < M_o$).

### Theorem 2.1 (Exact $D_4$ Orbit Completeness — Even & Odd $N$)
The dihedral symmetry group $D_4 = \langle T_{-}, T_{\text{alt}}, T_{\text{rev}} \rangle$ of order 8 acts on $\{-1, +1\}^N$ via:
- $T_{-}(c)_j = -c_j$ (global sign: $|g(-z)|$ unchanged, pointwise $|T_- g(e^{i\theta})| = |g(e^{i\theta})|$),
- $T_{\text{alt}}(c)_j = (-1)^j c_j$ (frequency shift $\theta \mapsto \theta + \pi$: $\max_\pm |g(\pm e^{i\theta})|$ invariant),
- $T_{\text{rev}}(c)_j = c_{N-1-j}$ (conjugation $z^{N-1} g(z^{-1})$: pointwise $|T_{\text{rev}} g(e^{i\theta})| = |g(e^{i\theta})|$).

Every $D_4$-orbit in $\{-1, +1\}^N$ contains **at least one** canonical representative $c$ satisfying:
1. **Sign normalization ($N \ge 2$):** $c_0 = +1$ and $c_1 = +1$ (equivalently $g_e[0] = g_o[0] = +1$).
   *Proof:* $\langle T_{-}, T_{\text{alt}} \rangle$ acts on $(g_e, g_o)$ as all four independent sign flips $(\pm g_e, \pm g_o)$, giving a unique representative with $g_e[0] = g_o[0] = +1$. Each normalized half $h \in \{+1\} \times \{-1,+1\}^{M-1}$ maps bijectively to `code(h)` $\in [0, 2^{M-1}-1]$ via bit $j-1 = \mathbf{1}[h[j] = +1]$.
2. **Reversal canonicalization:** Define for any sign-normalized half $h$ of length $M$:
   $$S(h) = \sum_{m=0}^{M-1} h[m], \quad U(h) = \sum_{m=0}^{M-1} (-1)^m h[m], \quad \mathrm{canon\_rev}(h) = \min\big(\mathrm{code}(h),\; \mathrm{code}(\pm \mathrm{rev}(h))\big),$$
   where $\pm \mathrm{rev}(h)$ denotes $h[M-1] \cdot \mathrm{rev}(h)$ (the unique sign-normalized reversal). Note that:
   - $|S(\pm \mathrm{rev}(h))| = |S(h)|$,
   - $U(\mathrm{rev}(h)) = (-1)^{M-1} U(h) \implies |U(\pm \mathrm{rev}(h))| = |U(h)|$,
   - $\mathrm{canon\_rev}(\pm \mathrm{rev}(h)) = \mathrm{canon\_rev}(h)$ (exact involution on $[0, 2^{M-1}-1]$).

   Therefore, the integer key $K(h) := (|S(h)|, |U(h)|, \mathrm{canon\_rev}(h))$ is **strictly invariant** under $h \mapsto \pm \mathrm{rev}(h)$.

   - **Case A (Even $N = 2M$, $M_e = M_o = M$):**
     Under $T_{\text{rev}}$, $2M - 1 - 2m = 2(M - 1 - m) + 1$ (odd) and $2M - 1 - (2m + 1) = 2(M - 1 - m)$ (even), so sign-normalized reversal swaps the halves:
     $$T_{\text{rev}}: (g_e, g_o) \longmapsto \big(\pm \mathrm{rev}(g_o),\; \pm \mathrm{rev}(g_e)\big), \qquad (K(g_e), K(g_o)) \longmapsto (K(g_o), K(g_e)).$$
     Restricting Stage 2 to pairs satisfying the **non-strict** lexicographic inequality
     $$K(g_o) \le K(g_e)$$
     guarantees coverage of every orbit: if $K(g_o) > K(g_e)$, its $T_{\text{rev}}$-image satisfies $K(g_o') < K(g_e')$; if $K(g_o) = K(g_e)$ (including all palindromic, skew-palindromic, $g_o = g_e$, and $g_o = \pm \mathrm{rev}(g_e)$ fixed points!), **both** $(g_e, g_o)$ and its $T_{\text{rev}}$-image are retained because `join_tile_kernel` uses `upper_bound` (`so_canon[j] <= se_canon[i]`).
   - **Case B (Odd $N = 2k + 1$, $M_e = k + 1$, $M_o = k$):**
     Under $T_{\text{rev}}$, $2k - 2m = 2(k - m)$ (even) and $2k - (2m + 1) = 2(k - 1 - m) + 1$ (odd), so sign-normalized reversal preserves parity:
     $$T_{\text{rev}}: (g_e, g_o) \longmapsto \big(\pm \mathrm{rev}(g_e),\; \pm \mathrm{rev}(g_o)\big).$$
     Restricting $g_e$ to $\mathrm{code}(g_e) = \mathrm{canon\_rev}(g_e)$ while leaving $g_o \in [0, 2^{M_o-1}-1]$ **completely unrestricted** covers every orbit: if $\mathrm{code}(g_e) > \mathrm{code}(\pm \mathrm{rev}(g_e))$, applying $T_{\text{rev}}$ produces $g_e' = \pm \mathrm{rev}(g_e)$ with $\mathrm{code}(g_e') = \mathrm{canon\_rev}(g_e')$ and valid $g_o' = \pm \mathrm{rev}(g_o) \in S_o$; if $g_e$ is palindromic or skew-palindromic ($\mathrm{code}(g_e) = \mathrm{code}(\pm \mathrm{rev}(g_e))$), $g_e$ is retained alongside all $g_o$. $\blacksquare$

*Empirical Verification (`verify.py` Test 1):* Exhaustive enumeration over all $\sum_{N=4}^{16} 2^N = 131{,}056$ polynomials ($16{,}635$ $D_4$-orbits, including all $380$ palindromic/skew-palindromic orbits and $359$ equal-`canon_rev` tie orbits) confirmed **0 missed orbits**.

---

## 3. Soundness of Every Pruning Inequality & Grid Discretization

Let $G \in \{64, 128, 256, \dots\}$ be an even grid parameter ($n_f = G/2 + 1$), and define $\theta_\ell = \pi \ell / G$ for $\ell = 0, \dots, G/2$. Suppose $g(z) = g_e(z^2) + z g_o(z^2)$ satisfies $\sup_{|z|=1} |g(z)|^2 \le M_{\text{bound}}$.

**Grid Discretization (Zero False Rejections):**
Because $\{\pm e^{i\theta_\ell} : \ell = 0, \dots, G/2\} \subset \{|z| = 1\}$ is a finite subset of the unit circle, every necessary bound enforced on the discrete grid $\theta_\ell$ is a **strict relaxation** of $\sup_{|z|=1} |g(z)|^2 \le M_{\text{bound}}$. Discretization can only admit extra coarse candidates (later eliminated by exact continuous evaluation), **never** falsely reject a valid polynomial.

### 3.1 Stage-1 Necessary Bounds (`stage1_find_codes_kernel`)
1. **DC / Nyquist Sum Bound ($z = \pm 1$):**
   $g(1) = S_e + S_o$ and $g(-1) = S_e - S_o \implies |S_e| + |S_o| = \max(|g(1)|, |g(-1)|) \le \sqrt{M_{\text{bound}}}$.
   Since $S_{\text{other}} \equiv M_{\text{other}} \pmod 2$, $|S_{\text{other}}| \ge m_{\text{other}} := (M_{\text{other}} \bmod 2)$, hence
   $$|S_{\text{this}}| \le \left\lfloor \sqrt{M_{\text{bound}}} + \varepsilon_{\text{safe}} - m_{\text{other}} + 10^{-9} \right\rfloor.$$
   *(Exact integer arithmetic via `__popc`; zero FP error in $|S|$.)*
2. **Quarter-Turn Bound ($z = \pm i$):**
   $g(\pm i) = g_e(-1) \pm i g_o(-1) = U_e \pm i U_o \implies U_e^2 + U_o^2 = |g(i)|^2 \le M_{\text{bound}}$.
   Since $|U_{\text{other}}| \ge m_{\text{other}}$,
   $$U_{\text{this}}^2 \le M_{\text{bound}} - m_{\text{other}}^2 + \varepsilon_{\text{safe}}.$$
   *(Exact integer arithmetic via `__popc(code ^ alt_flip_mask)`, where `alt_flip_mask = 0x55555555u & ((1u << (M_len - 1)) - 1u)` flips every odd index $j = 1, 3, 5, \dots$.)*
3. **Parallelogram Spectral Bound (all $\ell = 0, \dots, G/2$):**
   $$|g_e(e^{2i\theta_\ell})|^2 + |g_o(e^{2i\theta_\ell})|^2 = \frac{|g(e^{i\theta_\ell})|^2 + |g(-e^{i\theta_\ell})|^2}{2} \le M_{\text{bound}}.$$
   Since both terms are nonnegative, $|g_e(e^{2i\theta_\ell})|^2 \le M_{\text{bound}}$ and $|g_o(e^{2i\theta_\ell})|^2 \le M_{\text{bound}}$. Enforced with slack $M_{\text{safe}} = M_{\text{bound}} + \varepsilon_{\text{safe}}$.

### 3.2 Stage-2A Cell Compatibility & Phase-Projection Bitset (`build_tile_kernel`, `stage1_extract_meta_kernel`)
1. **2D $(|S|, |U|)$ Cell Filter:** Only pairs cells with $s_i + s_j \le \sqrt{M_{\text{bound}}} + \varepsilon_{\text{safe}}$ and $u_i^2 + u_j^2 \le M_{\text{bound}} + \varepsilon_{\text{safe}}$. Direct consequence of $z = \pm 1, \pm i$ above.
2. **Phase-Projection Law (792 separable `uint32` constraints):**
   At each sub-frequency $\ell = s \cdot \text{stride}$ ($s \in [0, 32]$, `n_sub <= 33`) and axis $\phi_a = a \pi / 4$ ($a \in \{0, 1, 2, 3\}$), let $w_e = g_e(e^{2i\theta_\ell})$ and $w_o = e^{i\theta_\ell} g_o(e^{2i\theta_\ell})$. Then:
   $$p_e + p_o := |\mathrm{Re}(e^{-i\phi_a} w_e)| + |\mathrm{Re}(e^{-i\phi_a} w_o)| = \max_{\pm} |\mathrm{Re}(e^{-i\phi_a} (w_e \pm w_o))| \le \max_{\pm} |g(\pm e^{i\theta_\ell})| \le \sqrt{M_{\text{bound}}} < B_{\text{safe\_proj}} := \sqrt{M_{\text{safe}}}.$$
   For each level $\alpha_\nu \in \{0.84, 0.74, 0.62, 0.50, 0.38, 0.26\}$ ($\beta_\nu = 1 - \alpha_\nu$), a pair $(i, j)$ is rejected by bitset constraint $(s, a, \nu)$ **only if**:
   $$\hat{p}_e > \alpha_\nu B_{\text{safe\_proj}} + 10^{-4} \quad \text{AND} \quad \hat{p}_o > (1 - \alpha_\nu) B_{\text{safe\_proj}} + 10^{-4}.$$
   Summing yields $\hat{p}_e + \hat{p}_o > B_{\text{safe\_proj}} + 2 \times 10^{-4}$. Thus any pair with exact $p_e + p_o \le \sqrt{M_{\text{safe}}}$ can only be pruned if floating-point error in $\hat{p}_e + \hat{p}_o$ exceeds **$2 \times 10^{-4}$**.

### 3.3 Stage-2B Exact Cross-Term Verification (`join_tile_kernel`)
For every bitset survivor $(i, j)$ and every $\ell \in \{0, \dots, G/2\}$, with $g_e(e^{2i\theta_\ell}) = r_i + i\, i_i$, $g_o(e^{2i\theta_\ell}) = r_j + i\, i_j$, $A_\ell = r_i r_j + i_i i_j$, $B_\ell = i_i r_j - r_i i_j$:
$$\max_{\pm} |g(\pm e^{i\theta_\ell})|^2 = (r_i^2 + i_i^2) + (r_j^2 + i_j^2) + 2 \left|\cos(\theta_\ell) A_\ell + \sin(\theta_\ell) B_\ell\right| \le M_{\text{safe}}.$$

---

## 4. Worst-Case IEEE-754 `float64` Error Budget vs. Hardened Margins (`N <= 56`)

Compilation uses strict IEEE-754 `double` (`nvcc -O3 -std=c++17 -shared -Xcompiler -fPIC`, strictly **no** `--use_fast_math`, `--ftz=true`, `--prec-div=false`, or `--prec-sqrt=false`). All trigonometric tables are precomputed once on host CPU (`libm` $\cos/\sin$, error $\le 0.51$ ULP); CUDA device kernels perform only IEEE-754 `double` additions, subtractions, multiplications, FMA (single rounding $\le 0.5 u$, strictly *tighter* than separate `*` and `+`), and `fabs`.

Let $u = 2^{-53} \approx 1.110223 \times 10^{-16}$ and $M_{\text{len}} \le 28$ ($N \le 56$). By Higham's forward error analysis (conservatively counting each FMA as $1 u$):

| Quantity | Worst-Case Analytical Bound ($N \le 56$) | Measured Max vs. 60-Digit Exact Decimal (`verify.py` Test 3) | Applied Margin (`v4.1`) | Safety Factor (Analytical / Empirical) |
| :--- | :---: | :---: | :---: | :---: |
| DFT component $\hat{r}, \hat{i}$ | $\le 1.81 \times 10^{-12}$ | $4.984 \times 10^{-14}$ | — | — |
| Stage-1 $\|h(e^{2i\theta_\ell})\|^2$ | $\le 2.50 \times 10^{-10}$ | $4.837 \times 10^{-13}$ | $\varepsilon_{\text{safe}} = 1.00 \times 10^{-6}$ | $4{,}000\times$ / $2.07 \times 10^{6}\times$ |
| Stage-2 $\|g(\pm e^{i\theta_\ell})\|^2$ | $\le 1.40 \times 10^{-9}$ | $7.198 \times 10^{-13}$ | $\varepsilon_{\text{safe}} = 1.00 \times 10^{-6}$ | $714\times$ / $1.39 \times 10^{6}\times$ |
| Phase-Projection $\hat{p}_e + \hat{p}_o$ | $\le 8.00 \times 10^{-12}$ | $5.156 \times 10^{-14}$ | $2 \times 10^{-4}$ above $\sqrt{M_{\text{safe}}}$ | $2.50 \times 10^{7}\times$ / $3.88 \times 10^{9}\times$ |
| Continuous Taylor-Bernstein $f_{\text{lo}}, f_{\text{ub}}$ | $\le 2.00 \times 10^{-11}$ | Verified via 50-digit Newton-polished supremum on $N=53,54,55(,56)$ | `FP_PAD` $= 1.00 \times 10^{-9}$ | $50\times$ |

---

## 5. Soundness of the Continuous Taylor-Bernstein Bracket (`eval_certified_supremum_general`)

Since $f(\theta) = |g(e^{i\theta})|^2 = N + 2 \sum_{k=1}^{N-1} R_k \cos(k\theta)$ is an even real trigonometric polynomial, $\sup_{\theta \in [0, 2\pi)} f(\theta) = \sup_{\theta \in [0, \pi]} f(\theta)$, and its second derivative satisfies uniformly:
$$|f''(\theta)| = \left|-2 \sum_{k=1}^{N-1} k^2 R_k \cos(k\theta)\right| \le 2 \sum_{k=1}^{N-1} k^2 |R_k| =: L_2 \in \mathbb{Z}_{\ge 0}.$$

**Lemma 5.1 (Interval Upper Bound):** On any closed interval $[a, b] \subset [0, \pi]$ of width $h = b - a$,
$$\max_{\theta \in [a, b]} f(\theta) \le \max\big(f(a), f(b)\big) + \frac{L_2}{8} h^2.$$
*Proof:* Let $\theta^* \in [a, b]$ attain $\max_{[a, b]} f$. If $\theta^* \in \{a, b\}$, the bound holds trivially. Otherwise $\theta^* \in (a, b)$ is an interior maximizer, so $f'(\theta^*) = 0$. Choosing the closer endpoint $e \in \{a, b\}$ with $|e - \theta^*| \le h/2$, Taylor's theorem gives $f(e) = f(\theta^*) + \frac{1}{2} f''(\xi)(e - \theta^*)^2 \ge f(\theta^*) - \frac{L_2}{8} h^2$, hence $f(\theta^*) \le f(e) + \frac{L_2}{8} h^2 \le \max(f(a), f(b)) + \frac{L_2}{8} h^2$. $\blacksquare$

Incorporating the explicit IEEE-754 evaluation guard `FP_PAD = 1e-9` (~50× above the worst-case Higham bound `2.0e-11` at $N = 56$) on both endpoints (pruning $[a, b]$ only when $\max(\hat{f}(a), \hat{f}(b)) + \frac{L_2}{8} h^2 + 10^{-9} \le \hat{f}_{\text{lo}} - 10^{-9}$ and returning $f_{\text{lo}}^{\text{rig}} = \hat{f}_{\text{lo}} - 10^{-9}$, $f_{\text{ub}}^{\text{rig}} = \hat{f}_{\text{ub}} + 10^{-9}$) guarantees $f_{\text{lo}}^{\text{rig}} \le \sup_{|z|=1} |g(z)|^2 \le f_{\text{ub}}^{\text{rig}}$ rigorously.

---

## 6. Hardening & Overflow Audit Checklist (`v4.2`, Applied After Blind `S-1` Audit Prior to `N = 56`)

The line-by-line internal audit (`v4.1`) plus independent blind `S-1` review (`v4.2`, `0 BLOCKER`, all `5 MODERATE` + `3 NIT` resolved) hardened 9 concrete safeguards before running `N = 56`:
1. **Stage-1 capacity bumped `32M -> 64M` (`max_out = 64000000ULL`, `max_cbuf = 64000000`):** Prevents Stage-1 survivor overflow at `N = 56` (`M = 28`, $2^{27} = 134.2\text{M}$ halves; peak VRAM `~10.9 GB` at `S = 64M` vs A100 `40/80 GB`).
2. **Immediate `CUDA_CHECK(cudaGetLastError())` after all 5 kernel launches (`S-1 MODERATE-1`):** Every `<<<...>>>` launch (`stage1_find_codes_kernel`, `stage1_extract_meta_kernel`, `gather_cids_kernel`, `build_tile_kernel`, `join_tile_kernel`) plus progress `cudaDeviceSynchronize()` is checked, eliminating any possibility of silent launch failure returning `hits = 0`.
3. **Unsigned 64-bit hit counter & Engine-3 overflow guard (`S-1 MODERATE-2`):** `d_hit_cnt` / `out_hit_count` upgraded from signed `int` to `unsigned long long` (`uint64_t`), preventing signed wrap-around; `engine3_bitset_mitm.py` raises `RuntimeError` if `nh > 20000`.
4. **Explicit domain/grid/epsilon & overflow return codes:** Rejects $N \notin [4, 64]$, $G < 32$ or odd $G$ or `n_sub > 33`, or `eps_safe < 1e-7` (`rc = -3`); returns `rc = -2` on Stage-1 overflow, `rc = -4` on Stage-2 hit overflow (`hc > max_hits`), and `rc = -5` on SHA-256 copy buffer overflow (`S > max_code_buf`).
5. **RAII `CudaEventGuard` (`S-1 NIT-2`):** Destroys `ev0, ev1, ev2` automatically on every early return path.
6. **Phase-Projection aligned to `B_safe_proj = sqrt(M_safe)`** across both `engine4_cuda_mitm.cu` and `engine3_bitset_mitm.py`, with `+1e-4` slack on each side (`>= 2e-4` total).
7. **Zero-initialized `sub_re[33] = {0.0}`, `sub_im[33] = {0.0}`** and verified 100% warp-uniform control flow across all `__ballot_sync` and `__any_sync` barriers.
8. **Conservative `FP_PAD = 1e-9` & 50-digit Newton-polished continuous verification (`S-1 MODERATE-5`):** Ensures `~50×` analytical margin above Higham's `2.0e-11` bound on `[f_lo, f_ub]` and verifies the true 50-digit continuous global peak sits strictly inside `[f_lo, f_ub]`.
9. **Pure-scratch primal scout ceiling (`S-1 MODERATE-4`) + dual-normalization provenance (`S-1 NIT-1`):** `primal_scout_ub` computes an unseeded upper bound (~3s CPU, safety-clamped so Stage-1 `|S|` never blows up), and every `v4.2` cert records both $M_n$ (`C_rms`) and $C^+$ intervals, `phase1_M_cap`, `phase1_hits`, `"IEEE-754 binary64 with FMA, NO --use_fast_math"`, and `engine_sha256`.

**Reproducibility Command (`env -i`, `0` GPU, ~11s):**
```bash
env -i NUMBA_NUM_THREADS=1 /opt/homebrew/bin/python3 verify.py
```

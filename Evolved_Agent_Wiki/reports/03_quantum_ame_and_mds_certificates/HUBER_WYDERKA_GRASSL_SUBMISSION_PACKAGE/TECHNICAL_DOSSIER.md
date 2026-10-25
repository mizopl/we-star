# Technical Dossier: Explicit AME Constructions ($n \le 20$), Purity Audit, and LaTeX Reference Table

This document provides the complete SHA-256 inventory, LaTeX table (`\begin{table*}...\end{table*}`), and structural classification accompanying the certificates in `certificates/*.json`.

---

## 1. Complete Inventory of Certificates and SHA-256 Checksums

| # | Target / Code | Parameters | Construction / Structure | Cuts / Minors Verified | Certificate File (`certificates/`) | SHA-256 (`first 16 hex`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | $\mathrm{AME}(9, 10)$ | $((9, 1, 5))_{10}$ | Closed-form $\mathbb{Q}(\zeta_5) \otimes \mathbb{F}_2$ tensor | $126 / 126$ cuts | `ame_9_10_certificate.json` | `9a17cd1e6d7fb101` |
| 2 | $\mathrm{AME}(11, 10)$ | $((11, 1, 6))_{10}$ | Closed-form $\mathbb{Q}(\zeta_5) \otimes \mathbb{F}_2$ tensor | $462 / 462$ cuts | `ame_11_10_certificate.json` | `2939f47d71d26b18` |
| 3 | $[[10, 2, 4]]_2$ | $d_{\mathrm{pure}}=6$ ($D=10$) | 2-qubit shortening of $[[12, 0, 6]]_2$ + Rains LP bounds | $252 / 252$ cuts ($64 I_{32}$) | `ame_10_10_shortened_binary_stabilizer_certificate.json` | `b720ce506d1839bf` |
| 4 | $[[13, 1, 7]]_5$ | $d_{\mathrm{pure}}=7$ (MDS) | Punctured & deleted Paley $C_{14}$ over $\mathbb{F}_5$ | $1,716 / 1,716$ cuts | `ame_13_5_quantum_mds_13_1_7_certificate.json` | `87f2c3d21cf8eb39` |
| 5 | $\mathrm{AME}(15, 7)$ | $[[15, 0, 8]]_7$ | Pure circulant graph state over $\mathbb{F}_7$: $r_0 = [0,1,5,4,2,1,0,0,0,0,1,2,4,5,1]$ | $6,435 / 6,435$ cuts | `ame_15_7_pure_circulant_certificate.json` | `0f52a39f008990cc` |
| 6 | $\mathrm{AME}(15, 8)$ | $[[15, 0, 8]]_8$ | Pure circulant graph state over $\mathbb{F}_8$: $a = [1,1,6,7,2,0,0]$ | $6,435 / 6,435$ cuts | `ame_15_8_pure_circulant_certificate.json` | `5748900e8ca81df5` |
| 7 | $\mathrm{AME}(15, 9)$ | $[[15, 0, 8]]_9$ | Pure circulant graph state over $\mathbb{F}_9$: $a = [1,3,4,5,1,0,0]$ | $6,435 / 6,435$ cuts | `ame_15_9_pure_circulant_certificate.json` | `86551558a3a40775` |
| 8 | $\mathrm{AME}(16, 11)$ | $[[16, 0, 9]]_{11}$ | Cayley constacyclic $[16,8,9]_{121}$ ($\lambda = 30$) $\to \mathbb{F}_{11}$ graph state | $12,870 / 12,870$ cuts | `ame_16_11_pure_hermitian_constacyclic_graph_certificate.json` | `0ea466b6539da517` |
| 9 | $\mathrm{AME}(16, 13)$ | $[[16, 0, 9]]_{13}$ | Cayley circulant $[16,8,9]_{169}$ ($\lambda = 1$) $\to \mathbb{F}_{13}$ graph state | $12,870 / 12,870$ cuts | `ame_16_13_pure_hermitian_constacyclic_graph_certificate.json` | `c344aec0c2f38aee` |
| 10 | $\mathrm{AME}(16, 16)$ | $[[16, 0, 9]]_{16}$ | Pure $D_8$ double-circulant graph state over $\mathbb{F}_{16}$ | $12,870 / 12,870$ cuts | `ame_16_16_pure_d8_double_circulant_certificate.json` | `4a23dd161482a245` |
| 11 | $\mathrm{AME}(16, 17)$ | $[[16, 0, 9]]_{17}$ | Twisted $D_8$ double-circulant over $\mathbb{F}_{17}$ ($\lambda = 3$) | $12,870 / 12,870$ cuts | `ame_16_17_pure_d8_double_circulant_certificate.json` | `24d0e8d97217f320` |
| 12 | $\mathrm{AME}(16, 19)$ | $[[16, 0, 9]]_{19}$ | Twisted $D_8$ double-circulant over $\mathbb{F}_{19}$ ($\lambda = 18$) | $12,870 / 12,870$ cuts | `ame_16_19_pure_d8_double_circulant_certificate.json` | `c868b813122ccb1e` |
| 13 | $\mathrm{AME}(17, 7)$ | $[[17, 0, 9]]_7$ | Sparse (deg-10) circulant graph state over $\mathbb{F}_7$: $a = [1,5,0,3,6,0,3,0]$ | $24,310 / 24,310$ cuts | `ame_17_7_pure_circulant_certificate.json` | `b68f2aac4f1d7297` |
| 14 | $\mathrm{AME}(17, 8)$ | $[[17, 0, 9]]_8$ | Pure circulant graph state over $\mathbb{F}_8$: $a = [1,2,5,1,5,2,2,2]$ | $24,310 / 24,310$ cuts | `ame_17_8_pure_circulant_certificate.json` | `0bc632480b2bfb3a` |
| 15 | $\mathrm{AME}(18, 7)$ | $[[18, 0, 10]]_7$ | Pure circulant graph state over $\mathbb{F}_7$: $a = [0,1,1,3,5,4,3,0,4]$ | $48,620 / 48,620$ cuts | `ame_18_7_pure_circulant_certificate.json` | `59b3292f2583484c` |
| 16 | $\mathrm{AME}(19, 16)$ | $[[19, 0, 10]]_{16}$ | Pure circulant graph state over $\mathbb{F}_{16}$: $a = [1,0,8,13,4,6,2,3,2]$ | $92,378 / 92,378$ cuts | `ame_19_16_pure_circulant_certificate.json` | `5dac5fa4efd3dc93` |
| 17 | $\mathrm{AME}(19, 17)$ | $[[19, 0, 10]]_{17}$ | Pure circulant graph state over $\mathbb{F}_{17}$: $a = [1,6,12,3,3,15,8,9,0]$ | $92,378 / 92,378$ cuts | `ame_19_17_pure_circulant_certificate.json` | `496c619a046592cd` |
| 18 | $\mathrm{AME}(19, 19)$ | $[[19, 0, 10]]_{19}$ | Pure circulant graph state over $\mathbb{F}_{19}$: $a = [1,12,14,7,9,8,15,17,15]$ | $92,378 / 92,378$ cuts | `ame_19_19_pure_circulant_certificate.json` | `afa20e21fc44d632` |
| 19 | Universal Paley ($n=13,14,17,18$) | $\mathrm{AME}(n, q)$ | Integer Paley $P_{13}/C_{14}$ and $P_{17}/C_{18}$ over $\mathbb{Z}$ | $\Delta_{13}, \Delta_{17}$ exact | `universal_paley_jacobsthal_ame_13_14_17_18_certificate.json` | `a442249dde030b73` |
| 20 | Universal Skew-Paley ($n=19,20$) | $\mathrm{AME}(n, q)$ | Skew-Jacobsthal $Q_{19}$ & conference $C_{20}$ over $\mathbb{Z}$ | $\Delta_{19}, \Delta_{20}$ exact | `universal_paley_jacobsthal_ame_19_20_certificate.json` | `0fc32a1ed4d418da` |
| 21 | 266-Cell Table Audit | $n, D \in [2,20]$ | 4-regime structural classification ($222/266$ resolved, $44$ open) | $266 / 266$ cells | `ame_table_n2_to_20_status_and_estimates.json` | `95e817c436014f28` |

---

## 2. LaTeX Table for Manuscript Inclusion

```latex
\begin{table*}[t]
\centering
\caption{Summary of newly constructed pure Absolutely Maximally Entangled ($\mathrm{AME}(n, q)$) graph states and quantum MDS codes ($d_{\mathrm{pure}} = \lfloor n/2 \rfloor + 1$). Each state is certified by exhaustive rank verification across all $\binom{n}{\lfloor n/2 \rfloor}$ bipartite cuts.}
\label{tab:new_ame_constructions}
\begin{tabular}{llllr}
\toprule
\textbf{State / Code} & \textbf{Parameters} & \textbf{Symmetry / Construction} & \textbf{Defining Vector / Generator} & \textbf{Cuts Verified} \\
\midrule
$\mathrm{AME}(9, 10)$ & $((9, 1, 5))_{10}$ & $\mathbb{Q}(\zeta_5)$ Closed-Form Tensor $\otimes \mathbb{F}_2$ & Exact algebraic unitary & $126 / 126$ \\
$\mathrm{AME}(11, 10)$ & $((11, 1, 6))_{10}$ & $\mathbb{Q}(\zeta_5)$ Closed-Form Tensor $\otimes \mathbb{F}_2$ & Exact algebraic unitary & $462 / 462$ \\
$[[13, 1, 7]]_5$ & $d_{\mathrm{pure}} = 7$ (MDS) & Punctured/Deleted Paley $C_{14}$ ($\mathbb{F}_5$) & $(I_{12}\mid b\ \mid\ D_{12}\mid 0) \pmod 5$ & $1,716 / 1,716$ \\
$\mathrm{AME}(13, q)$ & $[[13, 0, 7]]_q$ & Universal Paley $P_{13}$ over $\mathbb{Z}$ & $\gcd(q, 210) = 1$ ($q \in \{11,13,16,17,19\}$) & $1,716 / 1,716$ \\
$\mathrm{AME}(14, q)$ & $[[14, 0, 8]]_q$ & Universal Bordered Paley $C_{14}$ over $\mathbb{Z}$ & $\gcd(q, 210) = 1$ ($q \in \{9,11,13,16,17,19\}$) & $3,432 / 3,432$ \\
$\mathrm{AME}(15, 7)$ & $[[15, 0, 8]]_7$ & Pure Circulant Graph State ($\mathbb{F}_7$) & $a = [1, 5, 4, 2, 1, 0, 0]$ & $6,435 / 6,435$ \\
$\mathrm{AME}(15, 8)$ & $[[15, 0, 8]]_8$ & Pure Circulant Graph State ($\mathbb{F}_8$) & $a = [1, 1, 6, 7, 2, 0, 0]$ & $6,435 / 6,435$ \\
$\mathrm{AME}(15, 9)$ & $[[15, 0, 8]]_9$ & Pure Circulant Graph State ($\mathbb{F}_9$) & $a = [1, 3, 4, 5, 1, 0, 0]$ & $6,435 / 6,435$ \\
$\mathrm{AME}(16, 11)$ & $[[16, 0, 9]]_{11}$ & Cayley Constacyclic $[16,8,9]_{121} \to \mathbb{F}_{11}$ & $\lambda = 30$, $a_{\mathbb{F}_{121}} = [119,72,2,60,101,1,117,12]$ & $12,870 / 12,870$ \\
$\mathrm{AME}(16, 13)$ & $[[16, 0, 9]]_{13}$ & Cayley Circulant $[16,8,9]_{169} \to \mathbb{F}_{13}$ & $\lambda = 1$, $a_{\mathbb{F}_{169}} = [55,1,146,143,82,9,17,88]$ & $12,870 / 12,870$ \\
$\mathrm{AME}(16, 16)$ & $[[16, 0, 9]]_{16}$ & Pure $D_8$ Double-Circulant ($\mathbb{F}_{16}$) & $A_0 = [0,1,0,15,0,15,0,1]$, $B_0 = [0,11,1,12,4,5,3,9]$ & $12,870 / 12,870$ \\
$\mathrm{AME}(16, 17)$ & $[[16, 0, 9]]_{17}$ & Twisted $D_8$ Double-Circulant ($\mathbb{F}_{17}, \lambda=3$) & $A_0 = [0,13,11,15,4,15,11,13]$, $B_0 = [13,3,16,9,6,4,1,14]$ & $12,870 / 12,870$ \\
$\mathrm{AME}(16, 19)$ & $[[16, 0, 9]]_{19}$ & Twisted $D_8$ Double-Circulant ($\mathbb{F}_{19}, \lambda=18$) & $A_0 = [0,18,9,12,6,12,9,18]$, $B_0 = [15,7,8,2,9,11,8,7]$ & $12,870 / 12,870$ \\
$\mathrm{AME}(17, 7)$ & $[[17, 0, 9]]_7$ & Sparse Circulant Graph State ($\mathbb{F}_7$) & $a = [1, 5, 0, 3, 6, 0, 3, 0]$ & $24,310 / 24,310$ \\
$\mathrm{AME}(17, 8)$ & $[[17, 0, 9]]_8$ & Pure Circulant Graph State ($\mathbb{F}_8$) & $a = [1, 2, 5, 1, 5, 2, 2, 2]$ & $24,310 / 24,310$ \\
$\mathrm{AME}(17, q)$ & $[[17, 0, 9]]_q$ & Universal Paley $P_{17}$ over $\mathbb{Z}$ & $\gcd(q, 6) = 1$ ($q \in \{5,7,11,13,17,19\}$) & $24,310 / 24,310$ \\
$\mathrm{AME}(18, 7)$ & $[[18, 0, 10]]_7$ & Pure Circulant Graph State ($\mathbb{F}_7$) & $a = [0, 1, 1, 3, 5, 4, 3, 0, 4]$ & $48,620 / 48,620$ \\
$\mathrm{AME}(18, q)$ & $[[18, 0, 10]]_q$ & Universal Bordered Paley $C_{18}$ over $\mathbb{Z}$ & $\gcd(q, 1482) = 1$ ($q \in \{5,7,11,17\}$) & $48,620 / 48,620$ \\
$\mathrm{AME}(19, 16)$ & $[[19, 0, 10]]_{16}$ & Pure Circulant Graph State ($\mathbb{F}_{16}$) & $a = [1, 0, 8, 13, 4, 6, 2, 3, 2]$ & $92,378 / 92,378$ \\
$\mathrm{AME}(19, 17)$ & $[[19, 0, 10]]_{17}$ & Pure Circulant Graph State ($\mathbb{F}_{17}$) & $a = [1, 6, 12, 3, 3, 15, 8, 9, 0]$ & $92,378 / 92,378$ \\
$\mathrm{AME}(19, 19)$ & $[[19, 0, 10]]_{19}$ & Pure Circulant Graph State ($\mathbb{F}_{19}$) & $a = [1, 12, 14, 7, 9, 8, 15, 17, 15]$ & $92,378 / 92,378$ \\
\bottomrule
\end{tabular}
\end{table*}
```

---

## 3. Structural Regimes of the $n \le 20, D \le 20$ Table

1. **Regime I (Analytical Non-Existence, $122 / 266 = 45.86\%$):** Ruled out by the Rains shadow inequality, the Scott bound, Ball–MDS thresholds ($n \le D + 1$ for even $n$), and Krawtchouk LP weight identities.
2. **Regime II (Universal Paley–Jacobsthal Algebra over $\mathbb{Z}$):** A single arithmetic conference matrix over $\mathbb{Z}$ resolves all prime powers $q \nmid \Delta_n$ simultaneously at $n = 13, 14, 17, 18, 19, 20$.
3. **Regime III (Quadratic-Extension $\mathbb{F}_{q^2}$ Hermitian Self-Dual MDS & Twisted Dihedral Graph States):** Passing from symmetric graph states over $\mathbb{F}_q$ to Cayley $\lambda$-constacyclic unitary matrices $A_k = \mu(I_k - S)(I_k + S)^{-1}$ over $\mathbb{F}_{q^2}$ reduces generic minor singularity rates from $1/q$ to $1/q^2$, halves the maximum minor size via Jacobi's unitary identity ($r \le \lfloor k/2 \rfloor$), halves the orbit count via anti-diagonal transpose symmetry, and reduces back to an explicit symmetric graph state $\Gamma_{2k} = X^{-1} Z \pmod q$ over $\mathbb{F}_q$. With $\mathrm{AME}(16, 11)$ and $\mathrm{AME}(16, 13)$ resolved, $88 / 95 = 92.63\%$ of all cells in prime-power dimensions $D \in \{11, 13, 16, 17, 19\}$ for $n \le 20$ are now settled.
4. **Regime IV (Composite $D \in \{6, 10, 12, 14, 15, 18, 20\}$):** Governed by Kronecker tensor products above the shadow ceiling and Rains–Krawtchouk LP thresholds below.

# Target Dossier — `cryptocellar-truppenschluessel-1941`

- **Category:** `unbroken-ciphers` (16th distinct problem category, 19th bank target)
- **Disclosure:** `open`
- **Primary Source:** Frode Weierud's CryptoCellar (`https://www.cryptocellar.org/bgac/g-army-ts-messages.html`, `sha256: 58a057ab7c535edb3517e7d2159afd149b435879aa49bf8372ccaed21a1675af`, fetched `2026-10-20T22:15:37Z`) and Ostwald & Weierud (2021, *Cryptologia*, `https://www.cryptocellar.org/pubs/mcts.pdf`, `sha256: def54306cf0a88d0d9c181c3bebf0e5c5cec371cbbea451c6fb9081c7b56535d`).

## 1. Current Status (`NOTHING (progress)` — Run `2026-10-21-0015`)
- **Verified Software & Baseline:**
  - `attempts/lens2_p1_blind_garble_and_crib_unmix/code/benchmark_p1_and_crib.c` and `test_unmix_1407.c` verify 100% bit-exact encipherment and decipherment (`Enc(Dec(CT)) == CT`) across all 9 solved historical messages (`14.07.1941` `194/194` chars and `16.07.1941` `462/462` chars) from Ostwald & Weierud (2021).
  - Uncapped conditional 4-gram scoring (`T4_COND[abcd] = (T4[abcd] - 0.75 * T3[abc]) + T3_COND[bcd]` with `-32768` floor) eliminates the Two-Square unigram-overcounting trap and makes the true `14.07.1941` daily key a strict local and global maximum (`571,334`).
  - Combining `climb_crib_invariant` (`V12` cross-square row-pair vertical swaps + `H1/H2` intra-square column-pair horizontal swaps) with `climb_with_unmix` (`5,120`-move Row-Pair Subset Unmixer + `620`-move Col-Pair Subset Unmixer) recovers **`194 / 194` (`100.0%`)** of the `14.07.1941` plaintext (`571,334 / 571,334`) from a blind 7-bigram (`14`-char) signature crib at Sample 811 (`unmix_1407_exact_solve.txt`), and reaches `540,561 / 571,334` (`94.6%` of true score) from zero-crib random restarts.

## 2. Live Leads (`L1`)
- **`L1` — Uncapped Conditional 4-Gram Row-Pair Subset Unmixer + Crib Pinning (`test_unmix_1407.c`):**
  - Achieves `100.0%` (`194/194`) exact plaintext recovery on `14.07.1941` once a 6-to-7 bigram (`12–14` char) crib is pinned and phase-locked.
  - On `04.07.1941` (`8` messages, `682` letters), reconciling the 3-way consensus of the repeated 18-letter internal segment across `Nr. 90` (`HGZVUULVXKYOUULV`), `Nr. 91` (`VZHGZVUUAIXKYOGKEK`), and `Nr. 92` (`KYOQKEKVZHGZVUULV`)—and the 14-letter closing across `Nr. 90` (`NRODVLMQULHVKZ`) and `Nr. 91` (`RRODVLMQVLHFKZ`)—provides a direct path to a clean 9-bigram consensus crib (`VZHGZVUULVXKYOGKEK`) once the single-letter phase shift in `Nr. 92` is aligned.

## 3. Dead Ends & Falsified Hypotheses (`H1`, `H2`)
- **`H1` (Lens 1 — Fixed-Phase Multi-Day Rope Team without Inner Phase-Shift / Garble Decoding):**
  - `03.07.1941` (`Nr. 84, 85, 86`): Falsified because `Nr. 85 (HKMZI, 140 chars)` contains massive operator stutter (`HKMZIBLW` $\times 2$, `HRMCEPDD` $\times 2$, `EAXBND` $\times 2$, `OVDG` $\times 2$, `MERT` $\times 4$, `WDNB` $\times 4$) and `Nr. 84` (`30` chars) is an exact substring of `Nr. 86` (`38` chars), leaving only `124` unique phase-locked characters (`62` bigrams)—below the blind Two-Square unicity threshold.
  - `08.07.1941` (`Nr. 121, 123, 129, 130`, `274` chars): Algebraic bipartite union-find filtering on shared header `IASRZEDSTB` eliminates `ANXOBERKOM`, `GEFEQTSSTA`, `DIVISIONSG`, and `AUFKLAERUN` (`0` valid keys); unmixed hill-climbing stalls at `384,123` (`1,401.9/char`) due to the unlocated odd-length deletion breakpoint in `Nr. 123 (EHNPZ, 87 chars)` and garbled doubled proper names (`GZLZNL/GZLZQQL`, `OFCZSL/OFCPSL`, `GZSDWYKO/GZSDOYKO`).
  - `04.07.1941` (`8` messages, `682` chars): Direct even-phase hill-climbing stalls at `401,726` (`1,004.3/char`) because `Nr. 92` has an internal odd-phase shift prior to offset 68 (`KYOQKEKVZHGZVUULV`) and `VZHGZVUULVXKYOGKEK` has `0` algebraically valid keys without correcting 1–2 telegraph garbles.
- **`H2` (Lens 2 — Single-Message `p1` Blind Garble Benchmark & Softened `-1600` Floor):**
  - Digraphic Error Amplification: Under an `8.40%` (`20/238`) single-letter ciphertext garble rate, each garbled letter corrupts 1.8 plaintext letters on average, capping raw decryption accuracy of the **exact true key $(K_1, K_2)$** at **`85.7%` (`204/238`)** before any key search begins.
  - Single-Message Unicity Deficit: On single `60–100` letter messages (`37–41` bigrams) with random squares, blind unmixing finds spurious keys scoring higher than the true garbled key (`202,775` vs `~165,000`) with only `6.3%` (`15/238`) exact plaintext accuracy.
  - Softened Conditional Floor (`-850 / -1600`): Capping `T4_COND` at `-1600` reduces `14.07.1941` 7-bigram crib recovery from `100.0%` (`194/194`) to `42.8%` (`83/194`).

## 4. Next Concrete Question (`Q2`)
- **`Q2`:** Can a consensus-reconciled 9-bigram crib on `04.07.1941` (`VZHGZVUULVXKYOGKEK` + `NRODVLMQULHVKZ`, correcting `AI -> LV` in `Nr. 91` and `OUULV -> OGKEK` in `Nr. 90` and aligning the odd-phase suffix of `Nr. 92`) combined with uncapped `T4_COND` (`-32768` floor) and the `5,120`-move Row-Pair Subset Unmixer break `04.07.1941` (`682` letters)?

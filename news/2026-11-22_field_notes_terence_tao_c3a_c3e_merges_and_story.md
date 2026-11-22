# Field Notes #005 (`2026-11-22`) — Two Terence Tao Merges (`3 / 3` in `teorth/optimizationproblems`: `C_3e > 1.27255802` & Unasterisked `C_3a > 1.19230254`)

> **Date:** `2026-11-22` · **Authors:** `@mizopl` & **`we*`** (`PROOFER` Open-Science Lab)  
> **Repository:** [`mizopl/we-star`](https://github.com/mizopl/we-star) (`we* = me + agentic systems we* create + the feedback loop`)  
> **Upstream Merges:** [`teorth/optimizationproblems#236`](https://github.com/teorth/optimizationproblems/pull/236) (`2026-10-26`), [`#340`](https://github.com/teorth/optimizationproblems/pull/340) (`2026-11-22`), [`#339`](https://github.com/teorth/optimizationproblems/pull/339) (`2026-11-22`)  
> **Certificates:** [`mizopl/ghr-c3a-odd-base-finite-bound`](https://github.com/mizopl/ghr-c3a-odd-base-finite-bound) (`0.39s` `3a` & `< 0.1s` `3e` standalone Python verifiers)

---

## 0. Limitations First (`-0 Hype`)

Before celebrating, the exact boundaries of both results:

1. **Both problems remain open:** Known upper bounds stay far above the lower bounds (`C_3a <= 1.312373...` via `[K2026c]`; `C_3e <= 4/3 = 1.3333...` via `[FrPi73]`).
2. **Higher asterisked entries exist on `3a`:** On [`constants/3a.md`](https://github.com/teorth/optimizationproblems/blob/main/constants/3a.md), `[Syl2026]` (`1.19281555*`, `1.19359680*`) and `[K2026b]`'s limit (`1.19519192*`) sit above our unasterisked `1.19230254` and will take the top certified spot if independently replayed.
3. **Prior art credited explicitly:** The `(B = 17086, q = 27995)` odd-base tuple for `3a` was previously noted by Carson Olafson (`@carson-olaf`) in a comment on closed `PR #134`, and our `3e` carry-free projection uses `@carson-olaf`'s two-temperature `<4, 5>` numerical semigroup alphabet (`[O2026]`, `PR #148`) and Logan Kleinwaks's (`@kleinwaks`, `[K2026b]`) masked-digit framework.
4. **Records in live open tables are temporary:** Active benchmarks move fast — someone with a sharper alphabet or a new construction can overtake `1.27255802` tomorrow.

---

## 1. Why We Are Happy About Today's Merges

Today (`2026-11-22`), Terence Tao (`@teorth`) merged both of our remaining pull requests in [`teorth/optimizationproblems`](https://github.com/teorth/optimizationproblems):

- **[`PR #340`](https://github.com/teorth/optimizationproblems/pull/340) (`constants/3a.md`):** removed the asterisk (`*`) from our finite-depth bound **`[M2026]` `C_3a > 1.19230254`** (`N = 10^{13}, q = 27995`) after two independent from-scratch replays by Arhan Canli (`@arhancanli`) and R. Pinho (`@rpinho`). On the live main table, `1.19230254` currently stands as the highest unasterisked lower bound for `3a`.
- **[`PR #339`](https://github.com/teorth/optimizationproblems/pull/339) (`constants/3e.md`):** merged **`[M2026b]` `C_3e > 1.27255802`** (`B = 160, Q = 321, N = 10^{15}`, independently replayed from Theorems C1–C3 by `@arhancanli`) — the first published improvement over Hennecart–Robert–Yudin's 1999 simplex bound (`1.27155...`, `[HRY1999]`), on Problem 6.43 of `[GGSWT2025]` (where AlphaEvolve without human hints reached `~1.21`).

We have no illusions about how long constructive bounds stay on top of an active leaderboard. Even so, we are genuinely happy to share this moment: we do not run a supercluster — everything here was built and verified on a single `16 GB M1 laptop` — and seeing **`3 / 3` merged PRs** and two unasterisked entries on the front page of Terence Tao's repository is worth noting openly while they stand.

---

## 2. Which Constitution Lineage Achieved This — and How Long It Took

| Phase | Date | Constitution Lineage | Active Wall Time | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **`C_3a` (`#236`)** | `2026-10-18 / 19` | **`PROOFER v15`** (`rgraph.py` + pre-registered bet + 3-skeptic gate; archived in [`StartFresh_v16/`](../StartFresh_v16/)) | ~2 hours overnight (1st hour falsified carry-free `Q = 2B+1` edits; 2nd hour pivoted to odd controlled-carry `q = 27995` + `0.39s` integer-interval verifier) | Merged `2026-10-26` as `[M2026]` (`1.19230254*`), then unasterisked `2026-11-22` (`#340`) |
| **`C_3e` (`#339`)** | `2026-11-06` | **`CONSTITUTION v19`** ([`CONSTITUTION_v19.md`](../CONSTITUTION_v19.md) / [`StartFresh_v19/`](../StartFresh_v19/): post-mortem `LESSONS_LEARNED.md` + `Op-M1..Op-M7` assumption inversion) | `< 1` day (emerged directly while writing the post-mortem after `@arhancanli`'s replay of `#236`) | Merged `2026-11-22` as `[M2026b]` (`1.27255802`, unasterisked `#1` on `3e.md`) |

---

## 3. How the Collaboration Actually Worked

This campaign is a clean illustration of what **`we* = me + agentic systems + the feedback loop`** looks like in practice:

1. **Productive failure first (`v15`, `2026-10-18/19`):** The first hour of the `3a` run was a clean dead end — scanning glued semigroups inside the carry-free regime `Q = 2B+1` confirmed Kleinwaks's `1.19102809` was already optimal there. Logging that dead end in [`rgraph.py`](../StartFresh_v16/graphs/ancestral_v15_atlas/ghr-sum-difference-c3a.jsonl) forced the pivot to an odd controlled-carry base `q < 2B+1` (`q = 27995`), avoiding the self-inverse residue `q/2`.
2. **Designing for a 3-second replay:** `@mizopl` pushed for self-contained, zero-dependency Python verifiers (`0.39s` for `3a`, `< 0.1s` for `3e`, pure `128`-bit integer-interval arithmetic + Robbins–Stirling bounds) and explicit prior-art credit. That single engineering choice mattered more than brute-force depth: external reviewers could re-implement and check our `k = 1` table in seconds from our `README.md` alone, whereas deeper multi-GB `k = 3` tables stayed unverified.
3. **The external open-science loop birthed `C_3e`:** After `@elder-plinius` reviewed the math on `V3R1T4S#485` (`2026-11-03`) and `@arhancanli` published a 3-second from-scratch replay (`2026-11-05`), we stopped to write an honest [`LESSONS_LEARNED.md`](https://github.com/mizopl/ghr-c3a-odd-base-finite-bound/blob/main/LESSONS_LEARNED.md) comparing our method against `@carson-olaf`'s `[O2026]`. Asking *"which constraint disappears on `3e`?"* immediately showed that `C_3e` places no cap on `max(A)` — so elementary carry-free base `Q = 2B+1` gives a 3-theorem Freiman `2`-isomorphism beating `[HRY1999]` with zero cyclic compression.
4. **Independent peer review closed the loop:** `@arhancanli` replayed `3e` in 5 seconds (`quantavane-replays/c3e`) and caught four page-text inaccuracies (which we fixed before merge), `@rpinho` added a second independent 120-digit `Decimal` replay of `3a` (`math-certificates/replays/3a`), and Terence Tao merged both `#340` and `#339` today.

---

← **[Back to `news/` Index](./README.md)** · **[Back to `mizopl/we-star` README](../README.md)**

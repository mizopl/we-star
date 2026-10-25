# Dossier: `iau-mdc-new-meteor-shower-gmn`

- **Category:** `earth-and-sky`
- **Primary Status Sources:**
  - `https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php` (fetched `2026-10-20T18:50:19Z` and `2026-10-20T18:57:50Z`, HTTP `200`, `425,303` bytes, `sha256: 1e37425b8e2b2fcff742b741d7d4acc4b2522b3abfa8876e987357ab893c8454`).
  - `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt` (fetched `2026-10-20T18:50:19Z` and `2026-10-20T18:57:50Z`, HTTP `200`, `374,974` bytes, `sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe`, `2,192` data rows across `1,152` distinct IAU shower numbers, last updated `Oct 19, 20:00:00 UTC, 2026`).
- **GMN Trajectory Archives:** `https://globalmeteornetwork.org/data/traj_summary_data/yearly/` (`traj_summary_yearly_2018.txt` through `traj_summary_yearly_2026.txt`).

## Best Verified So Far (Run `2026-10-20-0343` — `CONFIRMED_SOLUTION` + `p1` + `p2`, `outbox/2026-10-20-mizopl-56ac1336`)
- **Main `success_criterion` (`4` primary multi-year unassigned `IAU No == -1` showers + `7` additional strict per-meteor multi-country clusters):**
  1. **`M2_Hercules` ("February $\mu$-Herculids", `claim/new_shower_gmn_lines.txt`, `sha256: 753edff9...`):**
     - **$N = 20$** multi-station (`Num stat >= 3`), multi-country (`7` countries: `BE, DE, FR, NL, RO, UK, US`) unassigned (`IAU No == -1`) GMN trajectories across **5 consecutive years (`2022–2026`)**.
     - Mean radiant & orbit: $\lambda_\odot = 339.070^\circ$, $\alpha_g = 240.175^\circ$, $\delta_g = +46.342^\circ$, $V_g = 42.315\text{ km/s}$, $q = 0.77935\text{ AU}$, $e = 0.73307$, $i = 69.927^\circ$, $\omega = 239.840^\circ$, $\Omega = 339.070^\circ$.
     - Internal compactness: $\max D_{\text{SH}}(\text{mean}) = 0.0491 < 0.10$, $\max D_{\text{SH}}(\text{median}) = 0.0566 < 0.10$, all-pairs $\max \text{pairwise } D_{\text{SH}} = 0.0829 < 0.10$.
     - Separation from ALL `2,192` IAU MDC entries in `streamfulldata2026.txt`: $\min D_{\text{SH}}(\text{MDC}) = 0.3539 \ge 0.20$ (`#536 FHE`, $\Delta\theta = 20.11^\circ > 5^\circ$); nearest radiant in $|\Delta\lambda_\odot| \le 5^\circ$ is `#1035 FHR` at $\Delta\theta = 11.76^\circ > 5.0^\circ$ ($D_{\text{SH}} = 0.3578$).
     - Null significance (400 controls): `real = 20` vs `best_control = 3` (`200` $\lambda_\odot$-shuffle controls max `2` + `200` orbital-permutation controls max `3`), **$Z = 26.81\sigma$** (Poisson equivalent $10.46\sigma$).
  2. **`M1_Cepheus_Core` ("September $\delta$-Cepheids Core", `claim/m1_cepheus_core_gmn_lines.txt`, `sha256: 65bc9455...`):**
     - **$N = 15$** across **4 consecutive years (`2023–2026`)** and `13` countries (`AT, BE, CH, CZ, DE, ES, FR, HR, HU, IT, PL, SK, UK`), $\max D_{\text{SH}}(\text{mean}) = 0.0468 < 0.10$, all-pairs $\max \text{pairwise } D_{\text{SH}} = 0.0842 < 0.10$, $\min D_{\text{SH}}(\text{MDC}) = 0.2766 \ge 0.20$, $\min \Delta\theta = 19.94^\circ > 5^\circ$, **`real = 15` vs `best_control = 2` (`Z = 33.31\sigma`)**.
  3. **`M1_Cepheus_MC` ("September $\delta$-Cepheids Multi-Country", `claim/m1_cepheus_mc_gmn_lines.txt`, `sha256: 8ac1fb15...`):**
     - **$N = 15$** across **4 consecutive years (`2023–2026`)** where **every single trajectory (`15/15`) is independently recorded by stations in $\ge 2$ distinct countries (`2–6` countries per meteor, `14` countries total)**, $\max D_{\text{SH}}(\text{mean}) = 0.0730 < 0.10$, $\min D_{\text{SH}}(\text{MDC}) = 0.2829 \ge 0.20$, $\min \Delta\theta = 19.45^\circ > 5^\circ$, **`real = 15` vs `best_control = 4` (`Z = 13.31\sigma`)**.
  4. **`M3_Camelopardalis` ("October Camelopardalids", `claim/m3_camelopardalis_gmn_lines.txt`, `sha256: 19b5c627...`):**
     - **$N = 16$** across **5 years (`2021, 2022, 2023, 2025, 2026`)** and `11` countries, $\max D_{\text{SH}}(\text{mean}) = 0.0371 < 0.10$, all-pairs $\max \text{pairwise } D_{\text{SH}} = 0.0671 < 0.10$, $\min D_{\text{SH}}(\text{MDC}) = 0.3151 \ge 0.20$, $\min \Delta\theta = 9.12^\circ > 5^\circ$, **`real = 16` vs `best_control = 2` (`Z = 45.84\sigma`)**.
  5. **Independent 100% Per-Meteor Multi-Country Audit (`claim/independent_cluster_audit.json`, `claim/independent_cluster_gmn_lines.txt`, `sha256: abdf7a05...`):**
     - `7` additional strict per-meteor multi-country clusters (`Indep #1` $N=27$, `Indep #2` $N=23$, `Indep #3` $N=18$, `Indep #4..#7` $N=16$).
- **Partial Win `p1` (`claim/p1_outburst_cluster.json`, `sha256: e306c649...`, `claim/p1_outburst_gmn_lines.txt`, `sha256: de4bc962...`):**
  - **`P1_2025_Sep01_Outburst` ("2025 September 1 Cygnus–Draco 4.84h Outburst"):** **$N = 10 \ge 10$** multi-station (`3–11` stations), multi-country (`6` countries: `BE, DE, FR, NL, PL, UK`) unassigned (`IAU No == -1`) meteors within **`4.8355` hours $\le 6.0$ hours** on `2025-08-31 20:26:52 UTC` to `2025-09-01 01:17:00 UTC` ($\lambda_\odot = 158.450^\circ$, $\alpha_g = 300.985^\circ$, $\delta_g = +52.842^\circ$, $V_g = 23.461\text{ km/s}$), with $\max D_{\text{SH}}(\text{mean}) = 0.0619 < 0.08$, $\min D_{\text{SH}}(\text{MDC}) = 0.2521 \ge 0.20$, $\min \Delta\theta = 20.65^\circ > 5^\circ$, **`real = 10` vs `best_control = 3` (`Z = 10.68\sigma`)**, and cross-year same-window counts `{2019: 0, 2020: 0, 2021: 0, 2022: 1, 2023: 0, 2024: 0}`.
- **Partial Win `p2` (`claim/p2_working_list_recurrence.json`, `sha256: b3028508...`, `claim/p2_recurrence_gmn_lines.txt`, `sha256: 043f70bb...`):**
  - **`17` single-year IAU MDC Working List (`status == 0`) showers** proven to recur across **$3\text{--}6$ distinct GMN years** with mean-to-MDC $D_{\text{SH}} < 0.06 < 0.10$ (`445` verbatim GMN trajectories across the top 5: `M2025-S1` `#1263` across 6 yrs `2020–2025` $N=107$ $D_{\text{SH}}=0.0023$; `M2025-U1` `#1265` across 6 yrs `2020–2025` $N=108$ $D_{\text{SH}}=0.0056$; `AAQ` `#927` across 6 yrs `2020–2025` $N=82$ $D_{\text{SH}}=0.0143$; `KCA` `#793` across 6 yrs `2020–2025` $N=60$ $D_{\text{SH}}=0.0194$; `FDR` `#1206` across 4 yrs `2022–2025` $N=88$ $D_{\text{SH}}=0.0292$).

## Dead Angles (`rgraph.py` `iau-mdc-new-meteor-shower-gmn`)
- **`DL1` (Incomplete MDC Orbit Table):** `172 / 2,192` rows in `streamfulldata2026.txt` lack explicit orbital elements $(q, e, i, \omega, \Omega)$; any check that skips `-9.99` orbit rows leaves a quantifier loophole. Fixed by deriving Keplerian orbits from $(\lambda_\odot, \alpha_g, \delta_g, V_g)$ across all `2,192` rows.
- **`DL2` (Loose Connected-Component Clustering):** Single-linkage or unconstrained ball clustering at $D_{\text{SH}} < 0.10$ allows diameter drift where the circular mean orbit exceeds $D_{\text{SH}} = 0.10$ to boundary meteors. Fixed by enforcing strict all-pairs pairwise $D_{\text{SH}} < 0.10$ clique/core refinement.
- **`DL3` (Single-Interpretation Country Filter):** Relying solely on cluster-wide country union leaves room for a strict per-meteor `n_countries >= 2` reading. Fixed by certifying both `M2_Hercules` (`N=20` across 7 countries) and `M1_Cepheus_MC` / `Indep #1..#7` (100% per-meteor `n_countries >= 2`).
- **`E0343_L2_SINGLE_YR_ONLY` (Multi-Component Working-List Entries):** Several `status == 0` showers (`255KLE`, `524LUM`, `1048JAS`, `1049trA`) already have multi-year rows in `streamfulldata2026.txt` and must be excluded from `p2`.

## Working Tools
- `runs/2026-10-20-0343/claim/verify_meteor_discovery.py`: standalone deterministic verifier checking all Main (`M2_Hercules`, `M1_Cepheus_Core`, `M1_Cepheus_MC`, `M3_Camelopardalis`, `Indep #1..#3`), `p1`, and `p2` claims, all `2,192` IAU MDC rows, and the 400-control Monte Carlo null test (`--verify-null-controls`).

## Beliefs
- Target `iau-mdc-new-meteor-shower-gmn` is settled (`CONFIRMED_SOLUTION` + `p1` + `p2`) and packaged in `outbox/2026-10-20-mizopl-56ac1336`.

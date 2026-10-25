# Dossier: `ccd-gupta-cobalt-clusters-n200`

- **Category:** `packings-physics` (7th distinct category)
- **Target:** Gupta cobalt clusters ($\text{Co}_N$, $N = 2..200$) — lower a putative global minimum on the Cambridge Cluster Database cobalt table or its posted improvements (`Co.zip`)
- **Primary Sources:**
  - `https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html` (`sha256: b1033b4142e8db518d0e9ef448c5e9d9e7fe651bc2088a0d54aad671eec030ef`)
  - `https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/points.tgz` (`sha256: bd568d308fc3944501e97fae1eb64d536769b59f0677f0e080246416c3c5f561`)
  - `https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/Co.zip` (`sha256: 28141c13e9658f901e6fa49228b38f3eca69a206f904a34043280f2ecebde9ca`)
  - L. Zhan, J. Z. Y. Chen, W.-K. Liu, and S. K. Lai, *J. Chem. Phys.* **122**, 244707 (2005), `doi:10.1063/1.1940028`

## Calibration & Baseline Audit (`p1`)

- **Exact Potential Parameters:** Cleri–Rosato (1993) cobalt parameters $A = 0.0950\text{ eV}$, $\xi = 1.4880\text{ eV}$, $p = 11.604$, $q = 2.286$, $r_0 = 1$ (no distance cutoff).
- **199 Table Files (`points/2..200`):** Coordinates are given to 6 decimal places. Raw evaluation matches `cobalt.html` within $2.938 \times 10^{-5}\text{ eV}$; local L-BFGS polishing of the 6-decimal truncation reproduces all 199 posted energies in `cobalt.html` to within $1.110 \times 10^{-6}\text{ eV}$ (`0` anomalies $> 10^{-5}\text{ eV}$ after polishing, `0` polish drops $> 10^{-4}\text{ eV}$).
- **10 `Co.zip` Files (`84, 95, 101, 113, 121, 122, 196, 197, 198, 200`):** Note that `cobalt.html` text contains a typo (`"196, 107, 198, 200"`), whereas `Co.zip` actually contains `Co197.txt` (`Energy.txt` lists `Co197 : -774.347649` vs `cobalt.html` `-774.3376731`). All 10 files reproduce `Energy.txt` to within $4.78 \times 10^{-7}\text{ eV}$.

## Literature Check

- OpenAlex / Crossref / arXiv citation & keyword audit of Zhan et al. (2005) (`W2085148121`, 57 citations) and `"cobalt clusters Gupta global minimum"`:
  - Lai, Huang, and Ni (2011, `doi:10.1021/jp110620x` / CCD `Co.zip`) contributed the 10 improved sizes (`84, 95, 101, 113, 121, 122, 196, 197, 198, 200`).
  - SaNSDE (2023, `doi:10.1021/acs.jcim.3c01331`) re-searched $\text{Co}_N, \text{Pt}_N, \text{Fe}_N$ ($N = 3..200$) against CCD and reported 13 lower-energy structures for $\text{Fe}_N$ but zero new lower-energy structures for $\text{Co}_N$ below the CCD + `Co.zip` baseline.
  - Zero open PRs or `TROPHY_CASE.md` entries in `elder-plinius/V3R1T4S` touch `ccd-gupta-cobalt-clusters-n200`.

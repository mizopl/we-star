# Dossier: covering-designs-record

## Best Verified So Far (2026-10-18)
- **`CONFIRMED_SOLUTION` — `C(94,13,5) <= 125,184`** (run `2026-10-18-0304`, packaged in `outbox/2026-10-18-mizopl-e1080bec/`, submitted as draft PR `#397`):
  - Explicit `(94,13,5)` covering design in `runs/2026-10-18-0304/claim/design_94_13_5.txt` (`sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`), `125,184` distinct 13-element blocks over `{0..93}`, 1-minimal (`0` redundant blocks), exhaustively verified over all $\binom{94}{5} = 54,891,018$ 5-subsets (`uncovered = 0`).
  - Strictly beats live Covering Repository (`129,203` at `2026-10-18T09:40:05Z`, by `4,019` blocks) and LJCR v1.2 (`129,337`, by `4,153` blocks). Passed 3-skeptic panel (`reproduce`, `novelty`, `criterion`) and `check_run.py`.
- **`CONFIRMED_SOLUTION` — `C(68,14,5) <= 15,675`** (run `2026-10-18-0304`, packaged in `outbox/2026-10-18-mizopl-2b72790b/`, submitted as draft PR `#398`):
  - Explicit `(68,14,5)` covering design in `runs/2026-10-18-0304/claim_68_14_5/design_68_14_5.txt` (`sha256 2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`, `632,514` bytes), `15,675` distinct 14-element blocks over `{1..68}`, 1-minimal (`0` redundant blocks; min uniquely covered 5-subsets per block = `6`), exhaustively verified over all $\binom{68}{5} = 10,424,128$ 5-subsets (`uncovered = 0`).
  - Strictly beats live Covering Repository (`16,004` at `2026-10-18T10:33:16Z`, by `329` blocks) and LJCR (`16,004`, by `329` blocks). Passed 3-skeptic panel (`panel/cell_68_14_5/{reproduce,novelty,criterion,gate}.md`) and `check_run.py --package`.
- **19 additional explicit designs (`PROMISING`, single-context, verified by `cover_check_bits` + `selfbreak`, unpanelled)** in `runs/2026-10-18-0304/attempts/{optimizer,extender,constructor}/result/`, all strictly beating live CR and LJCR:
  - `(80,16,6)`: `146,365` vs CR `155,960` (-9,595) — `attempts/optimizer/result/80-16-6.txt`
  - `(79,21,7)`: `147,717` vs CR `157,903` (-10,186) — `attempts/optimizer/result/79-21-7.txt`
  - `(65,17,7)`: `174,749` vs CR `183,815` (-9,066) — `attempts/optimizer/result/65-17-7.txt`
  - `(64,15,6)`: `58,044` vs CR `59,496` (-1,452) — `attempts/extender/result/64-15-6.txt`
  - `(81,11,5)`: `147,467` vs CR `148,485` (-1,018) — `attempts/optimizer/result/81-11-5.txt`
  - `(43,9,6)`: `150,739` vs CR `151,583` (-844) — `attempts/extender/result/43-9-6.txt`
  - `(96,18,5)`: `22,980` vs CR `23,699` (-719) — `attempts/extender/result/96-18-5.txt`
  - `(68,18,7)`: `173,095` vs CR `173,588` (-493) — `attempts/optimizer/result/68-18-7.txt`
  - `(61,12,6)`: `187,385` vs CR `187,869` (-484) — `attempts/optimizer/result/61-12-6.txt`
  - `(40,16,7)`: `7,251` vs CR `7,470` (-219) — `attempts/extender/result/40-16-7.txt`
  - `(65,23,6)`: `3,771` vs CR `3,989` (-218) — `attempts/extender/result/65-23,6.txt`
  - `(67,23,6)`: `4,447` vs CR `4,662` (-215) — `attempts/extender/result/67-23-6.txt`
  - `(57,15,6)`: `26,879` vs CR `27,043` (-164) — `attempts/extender/result/57-15-6.txt`
  - `(63,21,6)`: `5,246` vs CR `5,400` (-154) — `attempts/extender/result/63-21-6.txt`
  - `(64,23,6)`: `3,250` vs CR `3,394` (-144) — `attempts/extender/result/64-23-6.txt`
  - `(64,22,6)`: `4,252` vs CR `4,377` (-125) — `attempts/extender/result/64-22-6.txt`
  - `(41,16,7)`: `9,129` vs CR `9,198` (-69) — `attempts/extender/result/41-16-7.txt`
  - `(42,19,8)`: `9,463` vs CR `9,488` (-25) — `attempts/extender/result/42-19-8.txt`
  - `(60,21,6)`: `4,067` vs CR `4,084` (-17) — `attempts/extender/result/60-21-6.txt`

## Covered Search Spaces
- Two-part and iterated combining with per-$j$ $k_1$, whole-side tails, and segment terms across all on-disk LJCR ingredients ($v \le 50, b \le 20,000$) + trivial + local rules over all $(v,k,t)$ with $v \le 99, k \le 25, t \le 8$: exhaustive DP bound scan (`runs/2026-10-18-0304/attempts/extender/code/scan.py`), yielding 9 flags (all L2328SD1).

## Dead Angles
- **D2328SC1**: CR per-cell `history.aspx` pages return Cloudflare 403 to plain GET. Never fetch them; use `https://coveringrepository.com/download_archive_vkt.aspx` (single plain GET, whole $(v,k,t)$ archive).
- **D0304OP1**: Re-optimizing two-part split with padded smaller-$k$ or point-deleted larger-$v$ ingredients gives 0 gain over the RFLAG prediction on the 7 L2328SD1 cells.
- **D0304EX3**: Greedy redundant-block pruning of plain (non-nested) combining products on 29 near-miss cells (1–10 blocks above live CR) removes 0 blocks. Pruning only pays when terms overlap (e.g. padded/deduped or nested staircase builds) or after `merge.c`.
- **Prune static buffer overflow (`prune.c` in extender)**: `200,000`-block static limit overflowed on `(49,13,7)` (`203,362`) and `(66,13,6)` (`224,388`); allocate dynamically before running large cells.

## Live Leads
- **L0304EX1**: Panel and package additional top-margin cells from the 20 verified designs above (one cell per claim/run, re-fetching CR archive before each), or run the remaining ~371 optimistic staircase flags with $\binom{v}{t} \le 5 \times 10^9$ (`runs/2026-10-18-0304/attempts/extender/code/stair_list_rest.txt`) after dynamic allocation in `prune.c`.
- **L0304CO_CHUNK**: `(86,23,7)` (`139,766` vs CR `147,364`, $\binom{86}{7} = 5.37 \times 10^9$) and `(77,25,8)` (`159,179` vs CR `169,050`, $\binom{77}{8} = 2.1 \times 10^{10}$) are built in `attempts/constructor/result/PENDING-*.txt` and await chunked exhaustive verification.

## Working Tools
- `runs/2026-10-18-0304/tools/cover_check_bits` (C 1-bit-per-subset exhaustive checker) and `tools/cover_check.py` (numpy `uint8` exhaustive checker).
- `runs/2026-10-18-0304/attempts/optimizer/code/{build.py,prune.c,merge.c}` (generalized combining builder, conservative `uint8` saturating prune, pair-merge reduction).
- `runs/2026-10-18-0304/attempts/extender/code/{scan_stair.py,stair_build.py,stair_batch.py}` (nested staircase combining).

## Beliefs
- Generalized combining with per-$j$ block-size splits and nested staircase subsets + `merge.c` / `prune.c` reliably beats DP table entries on mid-to-large $v$ ($v \in [40, 96], t \in [5, 8]$) where LJCR/CR relied on unpruned two-part splits.

# Fast Matrix Multiplication (`ZT` / `Z` Rank Schemes & Addition-Reduced SLPs)

Machine-verified Fast Matrix Multiplication (`FMM`) schemes discovered using the **[`we*star`](https://github.com/mizopl/we-star)** human-AI autoresearch architecture (`CONSTITUTION v18`):

- **Machine-readable status index (Perminov `status.json` format):** [`status.json`](status.json)

## 1. Ten Ternary (`ZT`, $\{-1, 0, +1\}$) & Integer (`Z`) Rank Schemes (`zt_rank_schemes/`)

| Shape $\langle m, n, p \rangle$ | Ring | New Rank | Previous `ZT` Rank (`matmulcatalog` / `FMM-Lille`) | $\Delta_{\text{ZT}}$ | File |
| :--- | :---: | :---: | :---: | :---: | :--- |
| $\langle 6, 12, 14 \rangle$ | `ZT` | **`654`** | `666` | `-12` | [`zt_rank_schemes/6x12x14_m654_ZT.json`](zt_rank_schemes/6x12x14_m654_ZT.json) |
| $\langle 9, 10, 13 \rangle$ | `ZT` | **`763`** | `771` | `-8` | [`zt_rank_schemes/9x10x13_m763_ZT.json`](zt_rank_schemes/9x10x13_m763_ZT.json) |
| $\langle 9, 10, 16 \rangle$ | `ZT` | **`920`** | `924` | `-4` | [`zt_rank_schemes/9x10x16_m920_ZT.json`](zt_rank_schemes/9x10x16_m920_ZT.json) |
| $\langle 9, 12, 14 \rangle$ | `ZT` | **`954`** | `960` | `-6` | [`zt_rank_schemes/9x12x14_m954_ZT.json`](zt_rank_schemes/9x12x14_m954_ZT.json) |
| $\langle 10, 15, 15 \rangle$ | `ZT` | **`1389`** | `1395` | `-6` | [`zt_rank_schemes/10x15x15_m1389_ZT.json`](zt_rank_schemes/10x15x15_m1389_ZT.json) |
| $\langle 10, 15, 16 \rangle$ | `ZT` | **`1484`** | `1488` | `-4` | [`zt_rank_schemes/10x15x16_m1484_ZT.json`](zt_rank_schemes/10x15x16_m1484_ZT.json) |
| $\langle 11, 15, 16 \rangle$ | `ZT` | **`1629`** | `1641` | `-12` | [`zt_rank_schemes/11x15x16_m1629_ZT.json`](zt_rank_schemes/11x15x16_m1629_ZT.json) |
| $\langle 12, 13, 16 \rangle$ | `ZT` | **`1546`** | `1548` | `-2` | [`zt_rank_schemes/12x13x16_m1546_ZT.json`](zt_rank_schemes/12x13x16_m1546_ZT.json) |
| $\langle 12, 15, 15 \rangle$ | `ZT` | **`1640`** | `1650` | `-10` | [`zt_rank_schemes/12x15x15_m1640_ZT.json`](zt_rank_schemes/12x15x15_m1640_ZT.json) |
| $\langle 14, 15, 15 \rangle$ | `ZT` | **`1894`** | `1905` | `-11` | [`zt_rank_schemes/14x15x15_m1894_ZT.json`](zt_rank_schemes/14x15x15_m1894_ZT.json) |
| $\langle 12, 13, 16 \rangle$ | `Z` | **`1541`** | `1544` (`serendipitous_base`) | `-3` | [`zt_rank_schemes/12x13x16_m1541_Z.json`](zt_rank_schemes/12x13x16_m1541_Z.json) |

## 2. Addition-Reduced Straight-Line Programs (`slp_addition_reduced/`)

Contains 48 addition-reduced ternary straight-line programs (`*_ZT_reduced.json`) and the standalone C++17 Primal–Dual Tellegen ($W^T$) + `CL1` signed-cancellation reducer ([`slp_addition_reduced/clss_cl1_tellegen_reducer.cpp`](slp_addition_reduced/clss_cl1_tellegen_reducer.cpp)), including:
- `3x3x7_m49_cr167_cn404_ZT_reduced.json` (rank `49`, reduced additions `167`, naive `404`)
- `3x5x6_m68_cr245_cn494_ZT_reduced.json` (rank `68`, reduced additions `245`, naive `494` — also first `ZT` scheme at rank `68`, previously only known via AlphaEvolve `Z`)
- `3x5x7_m79_cr294_cn520_ZT_reduced.json` (rank `79`, reduced additions `294`, naive `520`)
- `5x6x6_m130_cr492_cn1662_ZT_reduced.json` (rank `130`, reduced additions `492`, naive `1662`)

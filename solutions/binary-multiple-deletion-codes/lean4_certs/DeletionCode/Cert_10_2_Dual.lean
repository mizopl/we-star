/-
  DeletionCode/Cert_10_2_Dual.lean — Pure-Kernel Recursive Block-Matrix Dual Proof for `(10, 2)`
  Source certificate: `cert_dual_10_2.json` (44 balls + 111 CLQ + 0 CG cuts)
  Exact integer bound: `795885064 / 39999994 = 19.897130 < 20` => `M_2(10) ≤ 19`
  Verified via `DeletionCode.RecDual.weak_duality_rec_fast` (ZERO flat ball tables, ZERO clique edge witnesses).
  Zero Mathlib, zero sorryAx, zero native_decide / Lean.ofReduceBool.
-/
import DeletionCode.Basic
import DeletionCode.DualLP
import DeletionCode.CutDual
import DeletionCode.RecDual
import DeletionCode.Cert_10_2_Dual.S0
import DeletionCode.Cert_10_2_Dual.S1
import DeletionCode.Cert_10_2_Dual.S2
import DeletionCode.Cert_10_2_Dual.S3

set_option maxRecDepth 65536
set_option maxHeartbeats 800000

namespace DeletionCode.RecDual

open DeletionCode
open DeletionCode.DualLP
open DeletionCode.CutDual
open DeletionCode.RecDual

def yList_10_2 : List (Nat × Nat) :=
  [(0, 20000000), (1, 9479364), (3, 14678988), (6, 4693224), (7, 14678988), (9, 1855242), (11, 1549216), (12, 6374667), (13, 1921480), (14, 7513381), (15, 5321012), (17, 1997600), (19, 4046031), (21, 687859), (22, 1727196), (23, 333236), (24, 3896126), (25, 4099985), (26, 1057363), (27, 78714), (28, 10369902), (30, 3000416), (33, 1075162), (34, 774495), (35, 3373706), (36, 5793), (38, 2722076), (41, 541934), (43, 748342), (44, 1808861), (49, 6490887), (50, 4425632), (60, 2299011), (61, 3550240), (62, 4428265), (65, 38637), (66, 24364), (70, 3823548), (85, 107242), (94, 784076), (97, 4341516), (110, 1685701), (113, 368), (126, 1606671)]

def clqs_10_2 : List (Nat × List Nat) := shard_10_2_s0 ++ shard_10_2_s1 ++ shard_10_2_s2 ++ shard_10_2_s3

private theorem hclqs_10_2 : ∀ c ∈ clqs_10_2, checkClqRec 10 2 c.2 = true := by
  intro c hc
  simp only [clqs_10_2, List.mem_append] at hc
  rcases hc with hc | h3
  case inr => exact hshard_10_2_s3 c h3
  rcases hc with hc | h2
  case inr => exact hshard_10_2_s2 c h2
  rcases hc with hc | h1
  case inr => exact hshard_10_2_s1 c h1
  exact hshard_10_2_s0 c hc

def cgs_10_2 : List (Nat × Nat × Nat × List Nat) :=
  []

private theorem hcgs_10_2 : ∀ cg ∈ cgs_10_2,
    checkCgRec (2 ^ (10 - 2)) cg.2.1 cg.2.2.1 cg.2.2.2 = true :=
  fun cg hcg => List.all_eq_true.mp (by rfl : cgs_10_2.all (fun cg => checkCgRec (2 ^ (10 - 2)) cg.2.1 cg.2.2.1 cg.2.2.2) = true) cg hcg

private theorem hwords_10_2 :
    (covSym4 10 2 yList_10_2 clqs_10_2 cgs_10_2).allGe 39999994 10 = true := by
  rfl

theorem cert_10_2_upper_bound {C : List Nat} (hC : IsValidDeletionCode 10 2 C) :
    C.length ≤ 19 :=
  weak_duality_rec_fast (n := 10) (s := 2) (Lmin := 39999994) (M := 19) (by decide)
    yList_10_2 (by rfl)
    clqs_10_2 hclqs_10_2
    cgs_10_2 hcgs_10_2
    hwords_10_2
    (by decide)
    hC

end DeletionCode.RecDual

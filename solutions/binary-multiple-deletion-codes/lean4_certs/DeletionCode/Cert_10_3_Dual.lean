/-
  DeletionCode/Cert_10_3_Dual.lean — Pure-Kernel Recursive Block-Matrix Dual Proof for `(10, 3)`
  Source certificate: `cert_dual_10_3_sparse.json` (7 balls + 14 CLQ + 23 CG cuts)
  Exact integer bound: `279759124 / 39999995 = 6.993979 < 7` => `M_3(10) ≤ 6`
  Verified via `DeletionCode.RecDual.weak_duality_rec_fast` (ZERO flat ball tables, ZERO clique edge witnesses).
  Zero Mathlib, zero sorryAx, zero native_decide / Lean.ofReduceBool.
-/
import DeletionCode.Basic
import DeletionCode.DualLP
import DeletionCode.CutDual
import DeletionCode.RecDual
import DeletionCode.Cert_10_3_Dual.S0
import DeletionCode.Cert_10_3_Dual.S1
import DeletionCode.Cert_10_3_Dual.S2
import DeletionCode.Cert_10_3_Dual.S3

set_option maxRecDepth 65536
set_option maxHeartbeats 1200000

namespace DeletionCode.RecDual

open DeletionCode
open DeletionCode.DualLP
open DeletionCode.CutDual
open DeletionCode.RecDual

def yList_10_3 : List (Nat × Nat) :=
  [(0, 20000000), (1, 3822591), (3, 3650255), (7, 9918092), (28, 477502), (30, 1217479), (54, 194962)]

def clqs_10_3 : List (Nat × List Nat) := shard_10_3_s0 ++ shard_10_3_s1 ++ shard_10_3_s2 ++ shard_10_3_s3

private theorem hclqs_10_3 : ∀ c ∈ clqs_10_3, checkClqRec 10 3 c.2 = true := by
  intro c hc
  simp only [clqs_10_3, List.mem_append] at hc
  rcases hc with hc | h3
  case inr => exact hshard_10_3_s3 c h3
  rcases hc with hc | h2
  case inr => exact hshard_10_3_s2 c h2
  rcases hc with hc | h1
  case inr => exact hshard_10_3_s1 c h1
  exact hshard_10_3_s0 c hc

def cgs_10_3 : List (Nat × Nat × Nat × List Nat) :=
  [
    (1074070, 2, 1, [25, 51, 53]),
    (518970, 2, 1, [26, 28, 44]),
    (40634, 2, 1, [26, 50, 58]),
    (486357, 2, 1, [67, 70, 71]),
    (3615570, 2, 1, [7, 14, 15]),
    (327917, 2, 1, [44, 84, 89]),
    (1333434, 2, 1, [1, 3, 17]),
    (5310667, 2, 1, [67, 71, 99]),
    (1811820, 2, 1, [28, 120, 124]),
    (447203, 2, 1, [102, 108, 110]),
    (1527465, 2, 1, [70, 76, 78]),
    (5684, 2, 1, [74, 85, 101]),
    (24599, 2, 1, [3, 7, 19]),
    (392620, 2, 1, [30, 60, 62]),
    (979663, 2, 1, [15, 29, 31]),
    (112438, 2, 1, [25, 28, 76]),
    (346420, 2, 1, [50, 98, 114]),
    (35643, 2, 1, [70, 75, 83]),
    (117305, 2, 1, [25, 50, 57]),
    (73374, 2, 1, [83, 99, 102]),
    (134933, 2, 1, [46, 54, 58]),
    (145987, 2, 1, [82, 102, 106]),
    (359869, 2, 1, [26, 42, 54])
  ]

private theorem hcgs_10_3 : ∀ cg ∈ cgs_10_3,
    checkCgRec (2 ^ (10 - 3)) cg.2.1 cg.2.2.1 cg.2.2.2 = true :=
  fun cg hcg => List.all_eq_true.mp (by rfl : cgs_10_3.all (fun cg => checkCgRec (2 ^ (10 - 3)) cg.2.1 cg.2.2.1 cg.2.2.2) = true) cg hcg

private theorem hwords_10_3 :
    (covSym4 10 3 yList_10_3 clqs_10_3 cgs_10_3).allGe 39999995 10 = true := by
  rfl

theorem cert_10_3_upper_bound {C : List Nat} (hC : IsValidDeletionCode 10 3 C) :
    C.length ≤ 6 :=
  weak_duality_rec_fast (n := 10) (s := 3) (Lmin := 39999995) (M := 6) (by decide)
    yList_10_3 (by rfl)
    clqs_10_3 hclqs_10_3
    cgs_10_3 hcgs_10_3
    hwords_10_3
    (by decide)
    hC

def cert_10_3_code : List Nat := [0, 15, 180, 819, 960, 1023]

theorem cert_10_3_valid : IsValidDeletionCode 10 3 cert_10_3_code :=
  checkCode3_sound 10 (by decide) (buildOwner3 10 cert_10_3_code) cert_10_3_code (by rfl)

theorem exact_opt_10_3 :
    (IsValidDeletionCode 10 3 cert_10_3_code ∧ cert_10_3_code.length = 6) ∧
    (∀ C : List Nat, IsValidDeletionCode 10 3 C → C.length ≤ 6) :=
  ⟨⟨cert_10_3_valid, rfl⟩, fun _ hC => cert_10_3_upper_bound hC⟩

end DeletionCode.RecDual

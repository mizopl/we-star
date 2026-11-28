/-
  DeletionCode/Cert_10_2_PSD/S1.lean — Pair-Check Shard 1/6 for `(10, 2)`
  Rows 19..39 (4032 unordered `D_2` orbit pairs across 8 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_10_2_PSD.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 19..20 (403 orbit pairs)
private theorem h_10_2_psd_s1_c0 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 19) = true := by rfl
-- Chunk 1: rows 21..23 (597 orbit pairs)
private theorem h_10_2_psd_s1_c1 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 21) = true := by rfl
-- Chunk 2: rows 24..26 (588 orbit pairs)
private theorem h_10_2_psd_s1_c2 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 24) = true := by rfl
-- Chunk 3: rows 27..29 (579 orbit pairs)
private theorem h_10_2_psd_s1_c3 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 27) = true := by rfl
-- Chunk 4: rows 30..32 (570 orbit pairs)
private theorem h_10_2_psd_s1_c4 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 30) = true := by rfl
-- Chunk 5: rows 33..35 (561 orbit pairs)
private theorem h_10_2_psd_s1_c5 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 33) = true := by rfl
-- Chunk 6: rows 36..38 (552 orbit pairs)
private theorem h_10_2_psd_s1_c6 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 36) = true := by rfl
-- Chunk 7: rows 39..39 (182 orbit pairs)
private theorem h_10_2_psd_s1_c7 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 1 (orbs_10_2_psd.drop 39) = true := by rfl

theorem hshard_10_2_psd_s1 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 21 (orbs_10_2_psd.drop 19) = true := by
  have h7 := h_10_2_psd_s1_c7
  have h6 : checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 36) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 1 (orbs_10_2_psd.drop 36) h_10_2_psd_s1_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 10 2 (- Int.ofNat 3989359) 7 (orbs_10_2_psd.drop 33) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 4 (orbs_10_2_psd.drop 33) h_10_2_psd_s1_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 10 2 (- Int.ofNat 3989359) 10 (orbs_10_2_psd.drop 30) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 7 (orbs_10_2_psd.drop 30) h_10_2_psd_s1_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 10 2 (- Int.ofNat 3989359) 13 (orbs_10_2_psd.drop 27) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 10 (orbs_10_2_psd.drop 27) h_10_2_psd_s1_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 10 2 (- Int.ofNat 3989359) 16 (orbs_10_2_psd.drop 24) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 13 (orbs_10_2_psd.drop 24) h_10_2_psd_s1_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 10 2 (- Int.ofNat 3989359) 19 (orbs_10_2_psd.drop 21) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 16 (orbs_10_2_psd.drop 21) h_10_2_psd_s1_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 10 2 (- Int.ofNat 3989359) 21 (orbs_10_2_psd.drop 19) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 19 (orbs_10_2_psd.drop 19) h_10_2_psd_s1_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

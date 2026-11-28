/-
  DeletionCode/Cert_10_2_PSD/S5.lean — Pair-Check Shard 5/6 for `(10, 2)`
  Rows 131..220 (4095 unordered `D_2` orbit pairs across 8 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_10_2_PSD.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 131..136 (525 orbit pairs)
private theorem h_10_2_psd_s5_c0 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 6 (orbs_10_2_psd.drop 131) = true := by rfl
-- Chunk 1: rows 137..143 (567 orbit pairs)
private theorem h_10_2_psd_s5_c1 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 7 (orbs_10_2_psd.drop 137) = true := by rfl
-- Chunk 2: rows 144..151 (588 orbit pairs)
private theorem h_10_2_psd_s5_c2 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 8 (orbs_10_2_psd.drop 144) = true := by rfl
-- Chunk 3: rows 152..160 (585 orbit pairs)
private theorem h_10_2_psd_s5_c3 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 9 (orbs_10_2_psd.drop 152) = true := by rfl
-- Chunk 4: rows 161..170 (555 orbit pairs)
private theorem h_10_2_psd_s5_c4 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 10 (orbs_10_2_psd.drop 161) = true := by rfl
-- Chunk 5: rows 171..183 (572 orbit pairs)
private theorem h_10_2_psd_s5_c5 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 13 (orbs_10_2_psd.drop 171) = true := by rfl
-- Chunk 6: rows 184..206 (598 orbit pairs)
private theorem h_10_2_psd_s5_c6 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 23 (orbs_10_2_psd.drop 184) = true := by rfl
-- Chunk 7 (tail): rows 207..220 (105 orbit pairs)
private theorem h_10_2_psd_s5_c7 :
    checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 207) = true := by rfl

theorem hshard_10_2_psd_s5 :
    checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 131) = true := by
  have h7 := h_10_2_psd_s5_c7
  have h6 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 184) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 23 (orbs_10_2_psd.drop 184) h_10_2_psd_s5_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 171) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 13 (orbs_10_2_psd.drop 171) h_10_2_psd_s5_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 161) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 10 (orbs_10_2_psd.drop 161) h_10_2_psd_s5_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 152) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 9 (orbs_10_2_psd.drop 152) h_10_2_psd_s5_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 144) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 8 (orbs_10_2_psd.drop 144) h_10_2_psd_s5_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 137) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 7 (orbs_10_2_psd.drop 137) h_10_2_psd_s5_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 131) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 6 (orbs_10_2_psd.drop 131) h_10_2_psd_s5_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

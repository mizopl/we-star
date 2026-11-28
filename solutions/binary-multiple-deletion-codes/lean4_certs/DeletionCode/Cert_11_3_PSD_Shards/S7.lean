/-
  DeletionCode/Cert_11_3_PSD_Shards/S7.lean — Pair-Check Shard 7/8 for `(11, 3)`
  Rows 210..320 (6216 unordered `D_2` orbit pairs across 8 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 210..216 (756 orbit pairs)
private theorem h_11_3_psd_s7_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 7 (orbs_11_3_psd.drop 210) = true := by rfl
-- Chunk 1: rows 217..224 (804 orbit pairs)
private theorem h_11_3_psd_s7_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 8 (orbs_11_3_psd.drop 217) = true := by rfl
-- Chunk 2: rows 225..233 (828 orbit pairs)
private theorem h_11_3_psd_s7_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 9 (orbs_11_3_psd.drop 225) = true := by rfl
-- Chunk 3: rows 234..243 (825 orbit pairs)
private theorem h_11_3_psd_s7_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 10 (orbs_11_3_psd.drop 234) = true := by rfl
-- Chunk 4: rows 244..254 (792 orbit pairs)
private theorem h_11_3_psd_s7_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 11 (orbs_11_3_psd.drop 244) = true := by rfl
-- Chunk 5: rows 255..268 (833 orbit pairs)
private theorem h_11_3_psd_s7_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 14 (orbs_11_3_psd.drop 255) = true := by rfl
-- Chunk 6: rows 269..288 (850 orbit pairs)
private theorem h_11_3_psd_s7_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 20 (orbs_11_3_psd.drop 269) = true := by rfl
-- Chunk 7 (tail): rows 289..320 (528 orbit pairs)
private theorem h_11_3_psd_s7_c7 :
    checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 289) = true := by rfl

theorem hshard_11_3_psd_s7 :
    checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 210) = true := by
  have h7 := h_11_3_psd_s7_c7
  have h6 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 269) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 20 (orbs_11_3_psd.drop 269) h_11_3_psd_s7_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 255) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 14 (orbs_11_3_psd.drop 255) h_11_3_psd_s7_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 244) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 11 (orbs_11_3_psd.drop 244) h_11_3_psd_s7_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 234) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 10 (orbs_11_3_psd.drop 234) h_11_3_psd_s7_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 225) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 9 (orbs_11_3_psd.drop 225) h_11_3_psd_s7_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 217) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 8 (orbs_11_3_psd.drop 217) h_11_3_psd_s7_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 210) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 7 (orbs_11_3_psd.drop 210) h_11_3_psd_s7_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

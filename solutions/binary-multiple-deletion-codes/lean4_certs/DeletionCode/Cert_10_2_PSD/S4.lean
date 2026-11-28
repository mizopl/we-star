/-
  DeletionCode/Cert_10_2_PSD/S4.lean — Pair-Check Shard 4/6 for `(10, 2)`
  Rows 93..130 (4161 unordered `D_2` orbit pairs across 8 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_10_2_PSD.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 93..96 (506 orbit pairs)
private theorem h_10_2_psd_s4_c0 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 93) = true := by rfl
-- Chunk 1: rows 97..100 (490 orbit pairs)
private theorem h_10_2_psd_s4_c1 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 97) = true := by rfl
-- Chunk 2: rows 101..105 (590 orbit pairs)
private theorem h_10_2_psd_s4_c2 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 5 (orbs_10_2_psd.drop 101) = true := by rfl
-- Chunk 3: rows 106..110 (565 orbit pairs)
private theorem h_10_2_psd_s4_c3 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 5 (orbs_10_2_psd.drop 106) = true := by rfl
-- Chunk 4: rows 111..115 (540 orbit pairs)
private theorem h_10_2_psd_s4_c4 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 5 (orbs_10_2_psd.drop 111) = true := by rfl
-- Chunk 5: rows 116..120 (515 orbit pairs)
private theorem h_10_2_psd_s4_c5 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 5 (orbs_10_2_psd.drop 116) = true := by rfl
-- Chunk 6: rows 121..126 (585 orbit pairs)
private theorem h_10_2_psd_s4_c6 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 6 (orbs_10_2_psd.drop 121) = true := by rfl
-- Chunk 7: rows 127..130 (370 orbit pairs)
private theorem h_10_2_psd_s4_c7 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 127) = true := by rfl

theorem hshard_10_2_psd_s4 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 38 (orbs_10_2_psd.drop 93) = true := by
  have h7 := h_10_2_psd_s4_c7
  have h6 : checkOrbRows 10 2 (- Int.ofNat 3989359) 10 (orbs_10_2_psd.drop 121) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 6 4 (orbs_10_2_psd.drop 121) h_10_2_psd_s4_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 10 2 (- Int.ofNat 3989359) 15 (orbs_10_2_psd.drop 116) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 5 10 (orbs_10_2_psd.drop 116) h_10_2_psd_s4_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 10 2 (- Int.ofNat 3989359) 20 (orbs_10_2_psd.drop 111) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 5 15 (orbs_10_2_psd.drop 111) h_10_2_psd_s4_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 10 2 (- Int.ofNat 3989359) 25 (orbs_10_2_psd.drop 106) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 5 20 (orbs_10_2_psd.drop 106) h_10_2_psd_s4_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 10 2 (- Int.ofNat 3989359) 30 (orbs_10_2_psd.drop 101) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 5 25 (orbs_10_2_psd.drop 101) h_10_2_psd_s4_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 10 2 (- Int.ofNat 3989359) 34 (orbs_10_2_psd.drop 97) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 4 30 (orbs_10_2_psd.drop 97) h_10_2_psd_s4_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 10 2 (- Int.ofNat 3989359) 38 (orbs_10_2_psd.drop 93) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 4 34 (orbs_10_2_psd.drop 93) h_10_2_psd_s4_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

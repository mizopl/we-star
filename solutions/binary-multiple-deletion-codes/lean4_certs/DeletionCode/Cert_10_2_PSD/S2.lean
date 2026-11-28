/-
  DeletionCode/Cert_10_2_PSD/S2.lean — Pair-Check Shard 2/6 for `(10, 2)`
  Rows 40..63 (4068 unordered `D_2` orbit pairs across 8 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_10_2_PSD.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 40..42 (540 orbit pairs)
private theorem h_10_2_psd_s2_c0 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 40) = true := by rfl
-- Chunk 1: rows 43..45 (531 orbit pairs)
private theorem h_10_2_psd_s2_c1 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 43) = true := by rfl
-- Chunk 2: rows 46..48 (522 orbit pairs)
private theorem h_10_2_psd_s2_c2 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 46) = true := by rfl
-- Chunk 3: rows 49..51 (513 orbit pairs)
private theorem h_10_2_psd_s2_c3 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 49) = true := by rfl
-- Chunk 4: rows 52..54 (504 orbit pairs)
private theorem h_10_2_psd_s2_c4 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 52) = true := by rfl
-- Chunk 5: rows 55..57 (495 orbit pairs)
private theorem h_10_2_psd_s2_c5 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 55) = true := by rfl
-- Chunk 6: rows 58..60 (486 orbit pairs)
private theorem h_10_2_psd_s2_c6 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 58) = true := by rfl
-- Chunk 7: rows 61..63 (477 orbit pairs)
private theorem h_10_2_psd_s2_c7 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 61) = true := by rfl

theorem hshard_10_2_psd_s2 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 24 (orbs_10_2_psd.drop 40) = true := by
  have h7 := h_10_2_psd_s2_c7
  have h6 : checkOrbRows 10 2 (- Int.ofNat 3989359) 6 (orbs_10_2_psd.drop 58) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 3 (orbs_10_2_psd.drop 58) h_10_2_psd_s2_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 10 2 (- Int.ofNat 3989359) 9 (orbs_10_2_psd.drop 55) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 6 (orbs_10_2_psd.drop 55) h_10_2_psd_s2_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 10 2 (- Int.ofNat 3989359) 12 (orbs_10_2_psd.drop 52) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 9 (orbs_10_2_psd.drop 52) h_10_2_psd_s2_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 10 2 (- Int.ofNat 3989359) 15 (orbs_10_2_psd.drop 49) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 12 (orbs_10_2_psd.drop 49) h_10_2_psd_s2_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 10 2 (- Int.ofNat 3989359) 18 (orbs_10_2_psd.drop 46) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 15 (orbs_10_2_psd.drop 46) h_10_2_psd_s2_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 10 2 (- Int.ofNat 3989359) 21 (orbs_10_2_psd.drop 43) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 18 (orbs_10_2_psd.drop 43) h_10_2_psd_s2_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 10 2 (- Int.ofNat 3989359) 24 (orbs_10_2_psd.drop 40) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 21 (orbs_10_2_psd.drop 40) h_10_2_psd_s2_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

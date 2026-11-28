/-
  DeletionCode/Cert_10_2_PSD/S3.lean — Pair-Check Shard 3/6 for `(10, 2)`
  Rows 64..92 (4147 unordered `D_2` orbit pairs across 8 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_10_2_PSD.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 64..66 (468 orbit pairs)
private theorem h_10_2_psd_s3_c0 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 64) = true := by rfl
-- Chunk 1: rows 67..69 (459 orbit pairs)
private theorem h_10_2_psd_s3_c1 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 67) = true := by rfl
-- Chunk 2: rows 70..73 (598 orbit pairs)
private theorem h_10_2_psd_s3_c2 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 70) = true := by rfl
-- Chunk 3: rows 74..77 (582 orbit pairs)
private theorem h_10_2_psd_s3_c3 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 74) = true := by rfl
-- Chunk 4: rows 78..81 (566 orbit pairs)
private theorem h_10_2_psd_s3_c4 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 78) = true := by rfl
-- Chunk 5: rows 82..85 (550 orbit pairs)
private theorem h_10_2_psd_s3_c5 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 82) = true := by rfl
-- Chunk 6: rows 86..89 (534 orbit pairs)
private theorem h_10_2_psd_s3_c6 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 4 (orbs_10_2_psd.drop 86) = true := by rfl
-- Chunk 7: rows 90..92 (390 orbit pairs)
private theorem h_10_2_psd_s3_c7 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 90) = true := by rfl

theorem hshard_10_2_psd_s3 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 29 (orbs_10_2_psd.drop 64) = true := by
  have h7 := h_10_2_psd_s3_c7
  have h6 : checkOrbRows 10 2 (- Int.ofNat 3989359) 7 (orbs_10_2_psd.drop 86) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 4 3 (orbs_10_2_psd.drop 86) h_10_2_psd_s3_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 10 2 (- Int.ofNat 3989359) 11 (orbs_10_2_psd.drop 82) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 4 7 (orbs_10_2_psd.drop 82) h_10_2_psd_s3_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 10 2 (- Int.ofNat 3989359) 15 (orbs_10_2_psd.drop 78) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 4 11 (orbs_10_2_psd.drop 78) h_10_2_psd_s3_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 10 2 (- Int.ofNat 3989359) 19 (orbs_10_2_psd.drop 74) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 4 15 (orbs_10_2_psd.drop 74) h_10_2_psd_s3_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 10 2 (- Int.ofNat 3989359) 23 (orbs_10_2_psd.drop 70) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 4 19 (orbs_10_2_psd.drop 70) h_10_2_psd_s3_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 10 2 (- Int.ofNat 3989359) 26 (orbs_10_2_psd.drop 67) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 23 (orbs_10_2_psd.drop 67) h_10_2_psd_s3_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 10 2 (- Int.ofNat 3989359) 29 (orbs_10_2_psd.drop 64) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 3 26 (orbs_10_2_psd.drop 64) h_10_2_psd_s3_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

/-
  DeletionCode/Cert_11_3_PSD_Shards/S2.lean — Pair-Check Shard 2/8 for `(11, 3)`
  Rows 43..66 (6396 unordered `D_2` orbit pairs across 8 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 43..45 (831 orbit pairs)
private theorem h_11_3_psd_s2_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 43) = true := by rfl
-- Chunk 1: rows 46..48 (822 orbit pairs)
private theorem h_11_3_psd_s2_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 46) = true := by rfl
-- Chunk 2: rows 49..51 (813 orbit pairs)
private theorem h_11_3_psd_s2_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 49) = true := by rfl
-- Chunk 3: rows 52..54 (804 orbit pairs)
private theorem h_11_3_psd_s2_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 52) = true := by rfl
-- Chunk 4: rows 55..57 (795 orbit pairs)
private theorem h_11_3_psd_s2_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 55) = true := by rfl
-- Chunk 5: rows 58..60 (786 orbit pairs)
private theorem h_11_3_psd_s2_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 58) = true := by rfl
-- Chunk 6: rows 61..63 (777 orbit pairs)
private theorem h_11_3_psd_s2_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 61) = true := by rfl
-- Chunk 7: rows 64..66 (768 orbit pairs)
private theorem h_11_3_psd_s2_c7 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 64) = true := by rfl

theorem hshard_11_3_psd_s2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 24 (orbs_11_3_psd.drop 43) = true := by
  have h7 := h_11_3_psd_s2_c7
  have h6 : checkOrbRows 11 3 (- Int.ofNat 6241589) 6 (orbs_11_3_psd.drop 61) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 3 (orbs_11_3_psd.drop 61) h_11_3_psd_s2_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 11 3 (- Int.ofNat 6241589) 9 (orbs_11_3_psd.drop 58) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 6 (orbs_11_3_psd.drop 58) h_11_3_psd_s2_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 11 3 (- Int.ofNat 6241589) 12 (orbs_11_3_psd.drop 55) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 9 (orbs_11_3_psd.drop 55) h_11_3_psd_s2_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 11 3 (- Int.ofNat 6241589) 15 (orbs_11_3_psd.drop 52) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 12 (orbs_11_3_psd.drop 52) h_11_3_psd_s2_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 11 3 (- Int.ofNat 6241589) 18 (orbs_11_3_psd.drop 49) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 15 (orbs_11_3_psd.drop 49) h_11_3_psd_s2_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 11 3 (- Int.ofNat 6241589) 21 (orbs_11_3_psd.drop 46) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 18 (orbs_11_3_psd.drop 46) h_11_3_psd_s2_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 11 3 (- Int.ofNat 6241589) 24 (orbs_11_3_psd.drop 43) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 21 (orbs_11_3_psd.drop 43) h_11_3_psd_s2_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

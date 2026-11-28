/-
  DeletionCode/Cert_11_3_PSD_Shards/S4.lean — Pair-Check Shard 4/8 for `(11, 3)`
  Rows 94..124 (6572 unordered `D_2` orbit pairs across 9 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 94..96 (678 orbit pairs)
private theorem h_11_3_psd_s4_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 94) = true := by rfl
-- Chunk 1: rows 97..99 (669 orbit pairs)
private theorem h_11_3_psd_s4_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 97) = true := by rfl
-- Chunk 2: rows 100..102 (660 orbit pairs)
private theorem h_11_3_psd_s4_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 100) = true := by rfl
-- Chunk 3: rows 103..105 (651 orbit pairs)
private theorem h_11_3_psd_s4_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 103) = true := by rfl
-- Chunk 4: rows 106..108 (642 orbit pairs)
private theorem h_11_3_psd_s4_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 106) = true := by rfl
-- Chunk 5: rows 109..112 (842 orbit pairs)
private theorem h_11_3_psd_s4_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 109) = true := by rfl
-- Chunk 6: rows 113..116 (826 orbit pairs)
private theorem h_11_3_psd_s4_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 113) = true := by rfl
-- Chunk 7: rows 117..120 (810 orbit pairs)
private theorem h_11_3_psd_s4_c7 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 117) = true := by rfl
-- Chunk 8: rows 121..124 (794 orbit pairs)
private theorem h_11_3_psd_s4_c8 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 121) = true := by rfl

theorem hshard_11_3_psd_s4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 31 (orbs_11_3_psd.drop 94) = true := by
  have h8 := h_11_3_psd_s4_c8
  have h7 : checkOrbRows 11 3 (- Int.ofNat 6241589) 8 (orbs_11_3_psd.drop 117) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 4 (orbs_11_3_psd.drop 117) h_11_3_psd_s4_c7
      (by simpa [List.drop_drop, Nat.add_comm] using h8)
  have h6 : checkOrbRows 11 3 (- Int.ofNat 6241589) 12 (orbs_11_3_psd.drop 113) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 8 (orbs_11_3_psd.drop 113) h_11_3_psd_s4_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 11 3 (- Int.ofNat 6241589) 16 (orbs_11_3_psd.drop 109) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 12 (orbs_11_3_psd.drop 109) h_11_3_psd_s4_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 11 3 (- Int.ofNat 6241589) 19 (orbs_11_3_psd.drop 106) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 16 (orbs_11_3_psd.drop 106) h_11_3_psd_s4_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 11 3 (- Int.ofNat 6241589) 22 (orbs_11_3_psd.drop 103) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 19 (orbs_11_3_psd.drop 103) h_11_3_psd_s4_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 11 3 (- Int.ofNat 6241589) 25 (orbs_11_3_psd.drop 100) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 22 (orbs_11_3_psd.drop 100) h_11_3_psd_s4_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 11 3 (- Int.ofNat 6241589) 28 (orbs_11_3_psd.drop 97) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 25 (orbs_11_3_psd.drop 97) h_11_3_psd_s4_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 11 3 (- Int.ofNat 6241589) 31 (orbs_11_3_psd.drop 94) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 28 (orbs_11_3_psd.drop 94) h_11_3_psd_s4_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

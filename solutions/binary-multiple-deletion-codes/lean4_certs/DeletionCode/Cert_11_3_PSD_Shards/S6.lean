/-
  DeletionCode/Cert_11_3_PSD_Shards/S6.lean — Pair-Check Shard 6/8 for `(11, 3)`
  Rows 162..209 (6504 unordered `D_2` orbit pairs across 9 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 162..166 (785 orbit pairs)
private theorem h_11_3_psd_s6_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 5 (orbs_11_3_psd.drop 162) = true := by rfl
-- Chunk 1: rows 167..171 (760 orbit pairs)
private theorem h_11_3_psd_s6_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 5 (orbs_11_3_psd.drop 167) = true := by rfl
-- Chunk 2: rows 172..176 (735 orbit pairs)
private theorem h_11_3_psd_s6_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 5 (orbs_11_3_psd.drop 172) = true := by rfl
-- Chunk 3: rows 177..182 (849 orbit pairs)
private theorem h_11_3_psd_s6_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 6 (orbs_11_3_psd.drop 177) = true := by rfl
-- Chunk 4: rows 183..188 (813 orbit pairs)
private theorem h_11_3_psd_s6_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 6 (orbs_11_3_psd.drop 183) = true := by rfl
-- Chunk 5: rows 189..194 (777 orbit pairs)
private theorem h_11_3_psd_s6_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 6 (orbs_11_3_psd.drop 189) = true := by rfl
-- Chunk 6: rows 195..200 (741 orbit pairs)
private theorem h_11_3_psd_s6_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 6 (orbs_11_3_psd.drop 195) = true := by rfl
-- Chunk 7: rows 201..207 (819 orbit pairs)
private theorem h_11_3_psd_s6_c7 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 7 (orbs_11_3_psd.drop 201) = true := by rfl
-- Chunk 8: rows 208..209 (225 orbit pairs)
private theorem h_11_3_psd_s6_c8 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 208) = true := by rfl

theorem hshard_11_3_psd_s6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 48 (orbs_11_3_psd.drop 162) = true := by
  have h8 := h_11_3_psd_s6_c8
  have h7 : checkOrbRows 11 3 (- Int.ofNat 6241589) 9 (orbs_11_3_psd.drop 201) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 7 2 (orbs_11_3_psd.drop 201) h_11_3_psd_s6_c7
      (by simpa [List.drop_drop, Nat.add_comm] using h8)
  have h6 : checkOrbRows 11 3 (- Int.ofNat 6241589) 15 (orbs_11_3_psd.drop 195) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 6 9 (orbs_11_3_psd.drop 195) h_11_3_psd_s6_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 11 3 (- Int.ofNat 6241589) 21 (orbs_11_3_psd.drop 189) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 6 15 (orbs_11_3_psd.drop 189) h_11_3_psd_s6_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 11 3 (- Int.ofNat 6241589) 27 (orbs_11_3_psd.drop 183) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 6 21 (orbs_11_3_psd.drop 183) h_11_3_psd_s6_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 11 3 (- Int.ofNat 6241589) 33 (orbs_11_3_psd.drop 177) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 6 27 (orbs_11_3_psd.drop 177) h_11_3_psd_s6_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 11 3 (- Int.ofNat 6241589) 38 (orbs_11_3_psd.drop 172) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 5 33 (orbs_11_3_psd.drop 172) h_11_3_psd_s6_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 11 3 (- Int.ofNat 6241589) 43 (orbs_11_3_psd.drop 167) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 5 38 (orbs_11_3_psd.drop 167) h_11_3_psd_s6_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 11 3 (- Int.ofNat 6241589) 48 (orbs_11_3_psd.drop 162) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 5 43 (orbs_11_3_psd.drop 162) h_11_3_psd_s6_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

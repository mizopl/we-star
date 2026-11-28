/-
  DeletionCode/Cert_11_3_PSD_Shards/S5.lean — Pair-Check Shard 5/8 for `(11, 3)`
  Rows 125..161 (6586 unordered `D_2` orbit pairs across 9 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 125..128 (778 orbit pairs)
private theorem h_11_3_psd_s5_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 125) = true := by rfl
-- Chunk 1: rows 129..132 (762 orbit pairs)
private theorem h_11_3_psd_s5_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 129) = true := by rfl
-- Chunk 2: rows 133..136 (746 orbit pairs)
private theorem h_11_3_psd_s5_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 133) = true := by rfl
-- Chunk 3: rows 137..140 (730 orbit pairs)
private theorem h_11_3_psd_s5_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 137) = true := by rfl
-- Chunk 4: rows 141..144 (714 orbit pairs)
private theorem h_11_3_psd_s5_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 141) = true := by rfl
-- Chunk 5: rows 145..148 (698 orbit pairs)
private theorem h_11_3_psd_s5_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 4 (orbs_11_3_psd.drop 145) = true := by rfl
-- Chunk 6: rows 149..153 (850 orbit pairs)
private theorem h_11_3_psd_s5_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 5 (orbs_11_3_psd.drop 149) = true := by rfl
-- Chunk 7: rows 154..158 (825 orbit pairs)
private theorem h_11_3_psd_s5_c7 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 5 (orbs_11_3_psd.drop 154) = true := by rfl
-- Chunk 8: rows 159..161 (483 orbit pairs)
private theorem h_11_3_psd_s5_c8 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 159) = true := by rfl

theorem hshard_11_3_psd_s5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 37 (orbs_11_3_psd.drop 125) = true := by
  have h8 := h_11_3_psd_s5_c8
  have h7 : checkOrbRows 11 3 (- Int.ofNat 6241589) 8 (orbs_11_3_psd.drop 154) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 5 3 (orbs_11_3_psd.drop 154) h_11_3_psd_s5_c7
      (by simpa [List.drop_drop, Nat.add_comm] using h8)
  have h6 : checkOrbRows 11 3 (- Int.ofNat 6241589) 13 (orbs_11_3_psd.drop 149) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 5 8 (orbs_11_3_psd.drop 149) h_11_3_psd_s5_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 11 3 (- Int.ofNat 6241589) 17 (orbs_11_3_psd.drop 145) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 13 (orbs_11_3_psd.drop 145) h_11_3_psd_s5_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 11 3 (- Int.ofNat 6241589) 21 (orbs_11_3_psd.drop 141) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 17 (orbs_11_3_psd.drop 141) h_11_3_psd_s5_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 11 3 (- Int.ofNat 6241589) 25 (orbs_11_3_psd.drop 137) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 21 (orbs_11_3_psd.drop 137) h_11_3_psd_s5_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 11 3 (- Int.ofNat 6241589) 29 (orbs_11_3_psd.drop 133) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 25 (orbs_11_3_psd.drop 133) h_11_3_psd_s5_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 11 3 (- Int.ofNat 6241589) 33 (orbs_11_3_psd.drop 129) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 29 (orbs_11_3_psd.drop 129) h_11_3_psd_s5_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 11 3 (- Int.ofNat 6241589) 37 (orbs_11_3_psd.drop 125) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 4 33 (orbs_11_3_psd.drop 125) h_11_3_psd_s5_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce

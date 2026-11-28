/-
  DeletionCode/Cert_12_3_PSD_Shards/L2.lean — FastOrb Link Shard 2/4 (orbits 400..599, chunked 25/thm)
-/
import DeletionCode.FastSchrijver
import DeletionCode.Cert_12_3_PSD_Shards.Data
import DeletionCode.Cert_12_3_PSD_Shards.KData

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.FastSchrijver

open DeletionCode.PeelReduce

private theorem hl_12_3_psd_l2_c0 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 400) (korbs_12_3_psd.drop 400) = true := by rfl
private theorem hl_12_3_psd_l2_c1 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 425) (korbs_12_3_psd.drop 425) = true := by rfl
private theorem hl_12_3_psd_l2_c2 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 450) (korbs_12_3_psd.drop 450) = true := by rfl
private theorem hl_12_3_psd_l2_c3 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 475) (korbs_12_3_psd.drop 475) = true := by rfl
private theorem hl_12_3_psd_l2_c4 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 500) (korbs_12_3_psd.drop 500) = true := by rfl
private theorem hl_12_3_psd_l2_c5 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 525) (korbs_12_3_psd.drop 525) = true := by rfl
private theorem hl_12_3_psd_l2_c6 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 550) (korbs_12_3_psd.drop 550) = true := by rfl
private theorem hl_12_3_psd_l2_c7 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 575) (korbs_12_3_psd.drop 575) = true := by rfl

theorem hlink_12_3_psd_l2 :
    checkFastLinkRows 12 3 512 16777216 512 200 (orbs_12_3_psd.drop 400) (korbs_12_3_psd.drop 400) = true := by
  have h7 := hl_12_3_psd_l2_c7
  have h6 : checkFastLinkRows 12 3 512 16777216 512 50 (orbs_12_3_psd.drop 550) (korbs_12_3_psd.drop 550) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 25 (orbs_12_3_psd.drop 550) (korbs_12_3_psd.drop 550) hl_12_3_psd_l2_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkFastLinkRows 12 3 512 16777216 512 75 (orbs_12_3_psd.drop 525) (korbs_12_3_psd.drop 525) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 50 (orbs_12_3_psd.drop 525) (korbs_12_3_psd.drop 525) hl_12_3_psd_l2_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkFastLinkRows 12 3 512 16777216 512 100 (orbs_12_3_psd.drop 500) (korbs_12_3_psd.drop 500) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 75 (orbs_12_3_psd.drop 500) (korbs_12_3_psd.drop 500) hl_12_3_psd_l2_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkFastLinkRows 12 3 512 16777216 512 125 (orbs_12_3_psd.drop 475) (korbs_12_3_psd.drop 475) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 100 (orbs_12_3_psd.drop 475) (korbs_12_3_psd.drop 475) hl_12_3_psd_l2_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkFastLinkRows 12 3 512 16777216 512 150 (orbs_12_3_psd.drop 450) (korbs_12_3_psd.drop 450) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 125 (orbs_12_3_psd.drop 450) (korbs_12_3_psd.drop 450) hl_12_3_psd_l2_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkFastLinkRows 12 3 512 16777216 512 175 (orbs_12_3_psd.drop 425) (korbs_12_3_psd.drop 425) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 150 (orbs_12_3_psd.drop 425) (korbs_12_3_psd.drop 425) hl_12_3_psd_l2_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkFastLinkRows 12 3 512 16777216 512 200 (orbs_12_3_psd.drop 400) (korbs_12_3_psd.drop 400) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 175 (orbs_12_3_psd.drop 400) (korbs_12_3_psd.drop 400) hl_12_3_psd_l2_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.FastSchrijver

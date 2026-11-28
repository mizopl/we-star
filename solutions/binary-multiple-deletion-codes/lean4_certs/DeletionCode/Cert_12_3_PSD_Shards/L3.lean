/-
  DeletionCode/Cert_12_3_PSD_Shards/L3.lean — FastOrb Link Shard 3/4 (orbits 600..796, chunked 25/thm)
-/
import DeletionCode.FastSchrijver
import DeletionCode.Cert_12_3_PSD_Shards.Data
import DeletionCode.Cert_12_3_PSD_Shards.KData

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.FastSchrijver

open DeletionCode.PeelReduce

private theorem hl_12_3_psd_l3_c0 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 600) (korbs_12_3_psd.drop 600) = true := by rfl
private theorem hl_12_3_psd_l3_c1 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 625) (korbs_12_3_psd.drop 625) = true := by rfl
private theorem hl_12_3_psd_l3_c2 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 650) (korbs_12_3_psd.drop 650) = true := by rfl
private theorem hl_12_3_psd_l3_c3 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 675) (korbs_12_3_psd.drop 675) = true := by rfl
private theorem hl_12_3_psd_l3_c4 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 700) (korbs_12_3_psd.drop 700) = true := by rfl
private theorem hl_12_3_psd_l3_c5 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 725) (korbs_12_3_psd.drop 725) = true := by rfl
private theorem hl_12_3_psd_l3_c6 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 750) (korbs_12_3_psd.drop 750) = true := by rfl
private theorem hl_12_3_psd_l3_c7 :
    checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 775) (korbs_12_3_psd.drop 775) = true := by rfl

theorem hlink_12_3_psd_l3 :
    checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 600) (korbs_12_3_psd.drop 600) = true := by
  have h7 := hl_12_3_psd_l3_c7
  have h6 : checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 750) (korbs_12_3_psd.drop 750) = true :=
    checkFastLink_of_rows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 750) (korbs_12_3_psd.drop 750) hl_12_3_psd_l3_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 725) (korbs_12_3_psd.drop 725) = true :=
    checkFastLink_of_rows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 725) (korbs_12_3_psd.drop 725) hl_12_3_psd_l3_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 700) (korbs_12_3_psd.drop 700) = true :=
    checkFastLink_of_rows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 700) (korbs_12_3_psd.drop 700) hl_12_3_psd_l3_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 675) (korbs_12_3_psd.drop 675) = true :=
    checkFastLink_of_rows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 675) (korbs_12_3_psd.drop 675) hl_12_3_psd_l3_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 650) (korbs_12_3_psd.drop 650) = true :=
    checkFastLink_of_rows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 650) (korbs_12_3_psd.drop 650) hl_12_3_psd_l3_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 625) (korbs_12_3_psd.drop 625) = true :=
    checkFastLink_of_rows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 625) (korbs_12_3_psd.drop 625) hl_12_3_psd_l3_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkFastLink 12 3 512 16777216 512 (orbs_12_3_psd.drop 600) (korbs_12_3_psd.drop 600) = true :=
    checkFastLink_of_rows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 600) (korbs_12_3_psd.drop 600) hl_12_3_psd_l3_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.FastSchrijver

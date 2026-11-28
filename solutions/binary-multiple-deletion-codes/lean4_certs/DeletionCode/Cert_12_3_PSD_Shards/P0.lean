/-
  DeletionCode/Cert_12_3_PSD_Shards/P0.lean — Flat-Wave Domination Shard (40 fast `D_2`-orbit step(s), wave 0)
-/
import DeletionCode.PeelReduce
import DeletionCode.Cert_12_3_PSD_Shards.Trees

set_option maxRecDepth 65536
set_option maxHeartbeats 1500000

namespace DeletionCode.PeelReduce

private def wave_12_3_psd_w0_p0_c0 : List (Nat × Nat) := [(23, 15), (27, 15), (29, 15), (39, 15), (43, 15), (45, 15), (46, 30), (47, 31), (51, 15), (53, 15), (54, 30), (55, 31), (59, 31), (71, 15), (75, 15), (77, 15), (78, 30), (79, 31), (83, 15), (85, 15)]
private theorem hwave_12_3_psd_w0_p0_c0 :
    wave_12_3_psd_w0_p0_c0.all (checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd) = true := by rfl
private def wave_12_3_psd_w0_p0_c1 : List (Nat × Nat) := [(86, 30), (87, 31), (89, 57), (90, 58), (91, 31), (92, 60), (93, 61), (94, 62), (95, 63), (103, 31), (107, 31), (109, 61), (110, 62), (111, 63), (119, 63), (143, 31), (151, 31), (155, 31), (157, 61), (158, 62)]
private theorem hwave_12_3_psd_w0_p0_c1 :
    wave_12_3_psd_w0_p0_c1.all (checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd) = true := by rfl

def wave_12_3_psd_w0_p0 : List (Nat × Nat) := wave_12_3_psd_w0_p0_c0 ++ wave_12_3_psd_w0_p0_c1

theorem hwave_12_3_psd_w0_p0 : ∀ st ∈ wave_12_3_psd_w0_p0, checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd st = true := by
  intro st hst
  simp only [wave_12_3_psd_w0_p0, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact List.all_eq_true.mp hwave_12_3_psd_w0_p0_c1 st hcur
  exact List.all_eq_true.mp hwave_12_3_psd_w0_p0_c0 st hst

end DeletionCode.PeelReduce

/-
  DeletionCode/Cert_12_3_PSD_Shards/P1.lean — Flat-Wave Domination Shard (40 fast `D_2`-orbit step(s), wave 0)
-/
import DeletionCode.PeelReduce
import DeletionCode.Cert_12_3_PSD_Shards.Trees

set_option maxRecDepth 65536
set_option maxHeartbeats 1500000

namespace DeletionCode.PeelReduce

private def wave_12_3_psd_w0_p1_c0 : List (Nat × Nat) := [(167, 31), (171, 31), (173, 61), (174, 62), (175, 63), (181, 117), (182, 118), (183, 63), (185, 121), (186, 122), (187, 123), (188, 124), (189, 125), (190, 126), (207, 63), (215, 63), (221, 125), (222, 126), (311, 63), (317, 125)]
private theorem hwave_12_3_psd_w0_p1_c0 :
    wave_12_3_psd_w0_p1_c0.all (checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd) = true := by rfl
private def wave_12_3_psd_w0_p1_c1 : List (Nat × Nat) := [(318, 126), (343, 63), (349, 125), (350, 126), (373, 245), (374, 246), (377, 249), (378, 250), (379, 251), (380, 252), (381, 253), (382, 254), (445, 253), (446, 254), (523, 519), (637, 253), (638, 254), (701, 253), (702, 254), (757, 501)]
private theorem hwave_12_3_psd_w0_p1_c1 :
    wave_12_3_psd_w0_p1_c1.all (checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd) = true := by rfl

def wave_12_3_psd_w0_p1 : List (Nat × Nat) := wave_12_3_psd_w0_p1_c0 ++ wave_12_3_psd_w0_p1_c1

theorem hwave_12_3_psd_w0_p1 : ∀ st ∈ wave_12_3_psd_w0_p1, checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd st = true := by
  intro st hst
  simp only [wave_12_3_psd_w0_p1, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact List.all_eq_true.mp hwave_12_3_psd_w0_p1_c1 st hcur
  exact List.all_eq_true.mp hwave_12_3_psd_w0_p1_c0 st hst

end DeletionCode.PeelReduce

/-
  DeletionCode/Cert_11_3_PSD_Shards/P1.lean — Flat-Wave Domination Shard (39 fast `D_2`-orbit step(s), wave 0)
-/
import DeletionCode.PeelReduce
import DeletionCode.Cert_11_3_PSD_Shards.Trees

set_option maxRecDepth 65536
set_option maxHeartbeats 1500000

namespace DeletionCode.PeelReduce

private def wave_11_3_psd_w0_p1_c0 : List (Nat × Nat) := [(174, 62), (181, 117), (182, 118), (185, 121), (186, 122), (187, 123), (188, 124), (189, 125), (190, 126), (221, 125), (222, 126), (267, 263), (317, 125), (318, 126), (349, 125), (350, 126), (373, 245), (374, 246), (377, 249), (378, 250)]
private theorem hwave_11_3_psd_w0_p1_c0 :
    wave_11_3_psd_w0_p1_c0.all (checkDomWaveStep 11 3 initTree_11_3_psd midTree_11_3_psd_0) = true := by rfl
private def wave_11_3_psd_w0_p1_c1 : List (Nat × Nat) := [(380, 252), (381, 253), (382, 254), (445, 253), (446, 254), (506, 508), (525, 519), (533, 519), (534, 526), (557, 541), (558, 542), (606, 574), (638, 254), (645, 643), (702, 254), (758, 502), (761, 505), (833, 897), (929, 961)]
private theorem hwave_11_3_psd_w0_p1_c1 :
    wave_11_3_psd_w0_p1_c1.all (checkDomWaveStep 11 3 initTree_11_3_psd midTree_11_3_psd_0) = true := by rfl

def wave_11_3_psd_w0_p1 : List (Nat × Nat) := wave_11_3_psd_w0_p1_c0 ++ wave_11_3_psd_w0_p1_c1

theorem hwave_11_3_psd_w0_p1 : ∀ st ∈ wave_11_3_psd_w0_p1, checkDomWaveStep 11 3 initTree_11_3_psd midTree_11_3_psd_0 st = true := by
  intro st hst
  simp only [wave_11_3_psd_w0_p1, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact List.all_eq_true.mp hwave_11_3_psd_w0_p1_c1 st hcur
  exact List.all_eq_true.mp hwave_11_3_psd_w0_p1_c0 st hst

end DeletionCode.PeelReduce

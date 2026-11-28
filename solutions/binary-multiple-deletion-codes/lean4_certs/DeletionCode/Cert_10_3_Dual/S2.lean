/-
  DeletionCode/Cert_10_3_Dual/S2.lean — Parallel Clique Verification Shard 3/4 for `(10, 3)`
  Contains 3 cliques (19,804 edges, 3 chunks).
  Zero Mathlib, zero sorryAx, zero native_decide.
-/
import DeletionCode.RecDual

set_option maxRecDepth 65536
set_option maxHeartbeats 1200000

namespace DeletionCode.RecDual

open DeletionCode
open DeletionCode.RecDual

private def clqGrp_10_3_s2_0 : List (Nat × List Nat) :=
  [
    (572714, [99, 101, 153, 163, 165, 169, 177, 195, 201, 202, 209, 211, 212, 213, 216, 218, 227, 230, 231, 233, 235, 237, 243, 281, 293, 305, 306, 310, 325, 329, 330, 331, 332, 337, 338, 339, 340, 341, 344, 345, 357, 359, 361, 362, 363, 365, 369, 370, 373, 402, 404, 405, 408, 409, 411, 412, 413, 419, 421, 425, 426, 427, 434, 435, 436, 437, 450, 453, 458, 459, 460, 461, 467, 469, 553, 561, 565, 585, 586, 589, 593, 596, 597, 598, 609, 610, 611, 612, 614, 618, 629, 677, 678, 681, 689, 691, 692, 693, 694, 697, 709, 713, 717, 725, 729, 742, 753, 793, 805, 812, 817, 819, 821, 841, 842, 843, 851, 853, 857, 870, 921])
  ]
private def clqGrp_10_3_s2_1 : List (Nat × List Nat) :=
  [
    (1147573, [170, 178, 197, 201, 209, 210, 278, 293, 294, 297, 298, 306, 329, 330, 337, 338, 401, 402, 404, 405, 406, 409, 418, 421, 422, 537, 547, 549, 550, 553, 554, 556, 561, 562, 564, 569, 579, 585, 586, 587, 588, 589, 593, 594, 595, 597, 600, 601, 602, 612, 613, 614, 617, 618, 625, 652, 657, 658, 659, 660, 662, 665, 666, 675, 676, 678, 681, 682, 706, 713, 715, 717, 723, 774, 777, 778, 780, 785, 786, 787, 788, 789, 790, 792, 794, 797, 803, 804, 805, 807, 809, 810, 811, 812, 813, 819, 834, 841, 843, 845, 846, 851, 853, 857, 870, 898, 900, 906, 907, 909, 915, 917, 918])
  ]
private def clqGrp_10_3_s2_2 : List (Nat × List Nat) :=
  [
    (673319, [58, 102, 106, 108, 114, 116, 117, 118, 122, 123, 125, 126, 156, 170, 172, 180, 181, 183, 184, 187, 189, 198, 202, 204, 206, 210, 211, 212, 213, 214, 216, 217, 218, 219, 228, 229, 231, 234, 235, 237, 238, 243, 245, 249, 250, 252, 286, 300, 310, 317, 318, 334, 342, 346, 348, 349, 358, 362, 363, 364, 365, 366, 371, 374, 376, 377, 380, 410, 413, 414, 426, 428, 429, 434, 437, 438, 442, 458, 460, 461, 462, 469, 473, 474, 476, 485, 486, 498, 570, 574, 618, 620, 621, 622, 627, 629, 633, 634, 636, 670, 686, 694, 700, 718, 726, 730, 742, 746, 754, 814, 822, 826])
  ]

def shard_10_3_s2 : List (Nat × List Nat) :=
  clqGrp_10_3_s2_0 ++ clqGrp_10_3_s2_1 ++ clqGrp_10_3_s2_2

private theorem hclq_10_3_s2_0 : clqGrp_10_3_s2_0.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s2_1 : clqGrp_10_3_s2_1.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s2_2 : clqGrp_10_3_s2_2.all (fun c => checkClqRec 10 3 c.2) = true := by rfl

theorem hshard_10_3_s2 : ∀ c ∈ shard_10_3_s2, checkClqRec 10 3 c.2 = true := by
  intro c hc
  simp only [shard_10_3_s2, List.mem_append] at hc
  rcases hc with hc | h2
  case inr => exact List.all_eq_true.mp hclq_10_3_s2_2 c h2
  rcases hc with hc | h1
  case inr => exact List.all_eq_true.mp hclq_10_3_s2_1 c h1
  exact List.all_eq_true.mp hclq_10_3_s2_0 c hc

end DeletionCode.RecDual

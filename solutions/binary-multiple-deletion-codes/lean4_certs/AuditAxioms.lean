/-
  AuditAxioms.lean — Machine-checkable axiom audit for every headline theorem in DeletionCode.
  All theorems must depend ONLY on standard Lean 4 axioms (subset of [propext, Classical.choice, Quot.sound]):
  ZERO sorryAx, ZERO Lean.ofReduceBool, ZERO Lean.trustCompiler!
-/
import DeletionCode
import Challenge

#print axioms DeletionCode.disjoint_delBall_iff_no_common_subseq
#print axioms DeletionCode.card_le_of_clique_cover
#print axioms DeletionCode.Cert_15_2.valid
#print axioms DeletionCode.Cert_15_2.inclusion_maximal
#print axioms DeletionCode.Cert_15_3.valid
#print axioms DeletionCode.Cert_15_3.inclusion_maximal
#print axioms DeletionCode.Cert_16_3.valid
#print axioms DeletionCode.Cert_16_3.inclusion_maximal
#print axioms DeletionCode.Cert_16_2.valid
#print axioms DeletionCode.Cert_16_2.inclusion_maximal
#print axioms DeletionCode.Cert_16_2_226.valid
#print axioms DeletionCode.DualLP.exact_opt_7_2
#print axioms DeletionCode.DualLP.exact_opt_9_3
#print axioms DeletionCode.DualLP.cert_16_3_klein4_invariant

#print axioms DeletionCode.RecDual.weak_duality_rec_fast
#print axioms DeletionCode.CutDual.exact_opt_8_2
#print axioms DeletionCode.RecDual.cert_10_2_upper_bound
#print axioms DeletionCode.RecDual.exact_opt_10_3
#print axioms DeletionCode.SchrijverPSD.weak_duality_schrijver_psd
#print axioms DeletionCode.SchrijverPSD.exact_opt_9_2
#print axioms DeletionCode.PeelReduce.weak_duality_peel_wave1_psd
#print axioms DeletionCode.PeelReduce.weak_duality_peel_wave2_psd
#print axioms DeletionCode.PeelReduce.cert_10_2_psd_upper_bound
#print axioms DeletionCode.PeelReduce.cert_10_2_psd_code_valid
#print axioms DeletionCode.PeelReduce.exact_opt_11_3_psd
#print axioms DeletionCode.FastSchrijver.weak_duality_fast_peel_wave1_psd
#print axioms DeletionCode.PeelReduce.cert_12_3_psd_upper_bound
#print axioms DeletionCode.PeelReduce.cert_12_3_psd_code_valid
#print axioms Challenge.exact_opt_8_2
#print axioms Challenge.upper_bound_10_2
#print axioms Challenge.exact_opt_10_3
#print axioms Challenge.exact_opt_9_2
#print axioms Challenge.upper_bound_10_2_psd
#print axioms Challenge.exact_opt_11_3
#print axioms Challenge.lower_bound_16_2_226
#print axioms Challenge.bounds_12_3

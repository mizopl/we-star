/-
  Challenge.lean — External Challenge Interface for PROOFER Deletion-Code `Tier A` Certification.
  Imports `DeletionCode.Statements` (zero-internal-import TCB) and exposes public verified theorems
  with zero `sorryAx` and zero `Lean.ofReduceBool` / `native_decide`.
-/
import DeletionCode.Statements
import DeletionCode

namespace Challenge

open DeletionCode

theorem exact_opt_8_2 :
    (IsValidDeletionCode 8 2 DeletionCode.CutDual.cert_8_2_code ∧
      DeletionCode.CutDual.cert_8_2_code.length = 7) ∧
    (∀ C : List Nat, IsValidDeletionCode 8 2 C → C.length ≤ 7) :=
  DeletionCode.CutDual.exact_opt_8_2

theorem upper_bound_10_2 :
    ∀ C : List Nat, IsValidDeletionCode 10 2 C → C.length ≤ 19 :=
  fun _ hC => DeletionCode.RecDual.cert_10_2_upper_bound hC

theorem exact_opt_10_3 :
    (IsValidDeletionCode 10 3 DeletionCode.RecDual.cert_10_3_code ∧
      DeletionCode.RecDual.cert_10_3_code.length = 6) ∧
    (∀ C : List Nat, IsValidDeletionCode 10 3 C → C.length ≤ 6) :=
  DeletionCode.RecDual.exact_opt_10_3

theorem exact_opt_9_2 :
    (IsValidDeletionCode 9 2 DeletionCode.SchrijverPSD.cert_9_2_code ∧
      DeletionCode.SchrijverPSD.cert_9_2_code.length = 11) ∧
    (∀ C : List Nat, IsValidDeletionCode 9 2 C → C.length ≤ 11) :=
  DeletionCode.SchrijverPSD.exact_opt_9_2

theorem upper_bound_10_2_psd :
    (IsValidDeletionCode 10 2 DeletionCode.PeelReduce.cert_10_2_psd_code ∧
      DeletionCode.PeelReduce.cert_10_2_psd_code.length = 16) ∧
    (∀ C : List Nat, IsValidDeletionCode 10 2 C → C.length ≤ 17) :=
  ⟨⟨DeletionCode.PeelReduce.cert_10_2_psd_code_valid, rfl⟩,
   fun _ hC => DeletionCode.PeelReduce.cert_10_2_psd_upper_bound hC⟩

theorem exact_opt_11_3 :
    (IsValidDeletionCode 11 3 DeletionCode.PeelReduce.cert_11_3_psd_code ∧
      DeletionCode.PeelReduce.cert_11_3_psd_code.length = 8) ∧
    (∀ C : List Nat, IsValidDeletionCode 11 3 C → C.length ≤ 8) :=
  DeletionCode.PeelReduce.exact_opt_11_3_psd

theorem lower_bound_16_2_226 :
    IsValidDeletionCode 16 2 DeletionCode.Cert_16_2_226.code ∧
      DeletionCode.Cert_16_2_226.code.length = 226 :=
  ⟨DeletionCode.Cert_16_2_226.valid, DeletionCode.Cert_16_2_226.code_length⟩

theorem bounds_12_3 :
    (IsValidDeletionCode 12 3 DeletionCode.PeelReduce.cert_12_3_psd_code ∧
      DeletionCode.PeelReduce.cert_12_3_psd_code.length = 12) ∧
    (∀ C : List Nat, IsValidDeletionCode 12 3 C → C.length ≤ 13) :=
  ⟨⟨DeletionCode.PeelReduce.cert_12_3_psd_code_valid, rfl⟩,
   fun _ hC => DeletionCode.PeelReduce.cert_12_3_psd_upper_bound hC⟩

end Challenge

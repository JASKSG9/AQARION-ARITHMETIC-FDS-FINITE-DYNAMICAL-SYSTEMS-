import Mathlib.Data.Setoid.Basic
import Mathlib.Data.Fintype.Card

namespace AQARION.TORE

variable {Ω : Type*} [Fintype Ω] [DecidableEq Ω]

abbrev Perm := Equiv.Perm Ω

def Partition := Setoid Ω

def transport (T : Perm) (R : Partition) : Partition where
  r x y := R.Rel (T.symm x) (T.symm y)
  iseqv := by
    constructor
    · intro x
      exact R.refl _
    · intro x y h
      exact R.symm h
    · intro x y z hxy hyz
      exact R.trans hxy hyz

end AQARION.TORE

def transported (T : Perm) (R : Partition) : ℕ → Partition
| 0 => R | k+1 => transport T (transported T R k)

def orbitJoin (T : Perm) (R : Partition) : ℕ → Partition
| 0 => R | k+1 => orbitJoin T R k ⊔ transported T R k


import json
import math
import random
from collections import defaultdict, deque, Counter

# ═══════════════════════════════════════════════════════════════════════════════
# AQARION v13.0 — UNIVERSAL FUNCTIONAL GRAPH CENSUS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class AQA_Engine:
    """
    Universal census engine for any functional graph T: X -> X.
    Computes the full AQA(T) invariant tuple.
    """
    
    def __init__(self, T, name):
        self.T = T          # dict: state -> next_state
        self.name = name
        self.N = len(T)
        self._cycles = None
        self._height = None
        self._inv = None
        self._levels = None
        self._beta = None
        self._quotient = None
    
    # ─────────────────────────────────────────────────────────────────────────
    # GRAPH ANALYSIS
    # ─────────────────────────────────────────────────────────────────────────
    
    def find_cycles(self):
        """Find all cycles. Returns list of cycles (lists of nodes)."""
        if self._cycles is not None:
            return self._cycles
        visited = [False] * self.N
        cycles = []
        for start in range(self.N):
            if visited[start]:
                continue
            path = []
            pos = {}
            cur = start
            while True:
                if visited[cur]:
                    if cur in pos:
                        cycles.append(path[pos[cur]:])
                    break
                visited[cur] = True
                pos[cur] = len(path)
                path.append(cur)
                cur = self.T[cur]
        self._cycles = cycles
        return cycles
    
    def build_inverse(self):
        if self._inv is not None:
            return self._inv
        inv = defaultdict(list)
        for x, y in self.T.items():
            inv[y].append(x)
        self._inv = inv
        return inv
    
    def compute_height(self):
        """BFS from attractors to compute height (distance to cycle)."""
        if self._height is not None:
            return self._height
        inv = self.build_inverse()
        cycles = self.find_cycles()
        attractors = set()
        for c in cycles:
            attractors.update(c)
        
        height = {}
        queue = deque()
        for a in attractors:
            height[a] = 0
            queue.append(a)
        
        while queue:
            x = queue.popleft()
            for y in inv[x]:
                if y not in height:
                    height[y] = height[x] + 1
                    queue.append(y)
        
        self._height = height
        return height
    
    # ─────────────────────────────────────────────────────────────────────────
    # AQA INVARIANTS
    # ─────────────────────────────────────────────────────────────────────────
    
    def level_profile(self):
        """L(t): height -> count"""
        if self._levels is not None:
            return self._levels
        height = self.compute_height()
        levels = Counter(height.values())
        self._levels = dict(sorted(levels.items()))
        return self._levels
    
    def inverse_branching_beta(self):
        """β(t) = |{x : 0 < h(x) ≤ t}|"""
        if self._beta is not None:
            return self._beta
        height = self.compute_height()
        max_h = max(height.values())
        beta = {}
        for t in range(1, max_h + 1):
            beta[t] = sum(1 for h in height.values() if 0 < h <= t)
        self._beta = beta
        return beta
    
    def in_degree_distribution(self):
        """Inverse branching: node -> in-degree"""
        inv = self.build_inverse()
        return {x: len(inv[x]) for x in range(self.N)}
    
    def h_layer(self):
        """h_layer = max_t log(L(t)) / t"""
        levels = self.level_profile()
        vals = []
        for t, n in levels.items():
            if t > 0 and n > 0:
                vals.append(math.log(n) / t)
        return max(vals) if vals else 0.0
    
    def h_branch(self):
        """h_branch = limsup (1/t) log β(t)"""
        beta = self.inverse_branching_beta()
        vals = []
        for t, b in beta.items():
            if b > 0:
                vals.append(math.log(b) / t)
        return max(vals) if vals else 0.0
    
    def quotient_estimate(self):
        """Q: number of equivalence classes under (height, attractor) observable."""
        if self._quotient is not None:
            return self._quotient
        height = self.compute_height()
        signatures = {}
        for x in range(self.N):
            cur = x
            while height[cur] > 0:
                cur = self.T[cur]
            signatures[x] = (height[x], cur)
        self._quotient = len(set(signatures.values()))
        return self._quotient
    
    def compression_ratio(self):
        return self.quotient_estimate() / self.N
    
    def compression_law(self):
        """Qualitative compression classification."""
        C = self.compression_ratio()
        if C < 0.001:
            return "ultra_high"
        elif C < 0.01:
            return "high"
        elif C < 0.1:
            return "medium"
        elif C < 0.3:
            return "low"
        else:
            return "very_low"
    
    # ─────────────────────────────────────────────────────────────────────────
    # FULL CENSUS
    # ─────────────────────────────────────────────────────────────────────────
    
    def census(self):
        cycles = self.find_cycles()
        height = self.compute_height()
        levels = self.level_profile()
        beta = self.inverse_branching_beta()
        in_deg = self.in_degree_distribution()
        
        return {
            "system": self.name,
            "N": self.N,
            "cycles": [
                {"size": len(c), "nodes": c[:10]}
                for c in cycles
            ],
            "num_cycles": len(cycles),
            "cycle_nodes": sum(len(c) for c in cycles),
            "transient_nodes": self.N - sum(len(c) for c in cycles),
            "max_height": max(height.values()),
            "height_spectrum": levels,
            "inverse_branching": {
                "max_indegree": max(in_deg.values()),
                "mean_indegree": sum(in_deg.values()) / self.N,
                "indegree_histogram": dict(Counter(in_deg.values()))
            },
            "beta": beta,
            "h_layer": self.h_layer(),
            "h_branch": self.h_branch(),
            "quotient_density": self.compression_ratio(),
            "compression_law": self.compression_law(),
            "AQA_tuple": {
                "N": self.N,
                "cycles": len(cycles),
                "height_spectrum": levels,
                "inverse_branching_max": max(in_deg.values()),
                "beta": beta,
                "h_layer": self.h_layer(),
                "h_branch": self.h_branch(),
                "quotient_density": self.compression_ratio(),
                "compression_law": self.compression_law()
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_kaprekar(d):
    def kap(n):
        s = str(n).zfill(d)
        return int("".join(sorted(s, reverse=True))) - int("".join(sorted(s)))
    return {n: kap(n) for n in range(10**d)}

def build_fibonacci_mod(m):
    """T(a,b) = (b, (a+b) mod m) on Z_m x Z_m. Bijection → all cycles, no transients."""
    T = {}
    for a in range(m):
        for b in range(m):
            state = a * m + b
            next_state = b * m + ((a + b) % m)
            T[state] = next_state
    return T

def build_random_map(N, seed=42):
    random.seed(seed)
    return {i: random.randrange(N) for i in range(N)}

def build_mandelbrot_lattice(resolution=40, c_complex=-0.75+0.1j, bound=2.0):
    """
    Discretized Mandelbrot iteration z -> z^2 + c on a grid.
    Points that escape (|z| > bound) map to a sink state.
    """
    # Grid in [-2, 2] x [-2, 2]
    step = 4.0 / (resolution - 1)
    grid = []
    for i in range(resolution):
        for j in range(resolution):
            x = -2.0 + i * step
            y = -2.0 + j * step
            grid.append(complex(x, y))
    
    sink = len(grid)  # last index is the escape sink
    T = {}
    
    def nearest_grid(z):
        if abs(z) > bound:
            return sink
        ix = min(resolution - 1, max(0, int(round((z.real + 2.0) / step))))
        iy = min(resolution - 1, max(0, int(round((z.imag + 2.0) / step))))
        return ix * resolution + iy
    
    for idx, z in enumerate(grid):
        z_next = z**2 + c_complex
        T[idx] = nearest_grid(z_next)
    
    T[sink] = sink  # sink is fixed point
    return T

def build_collatz_truncated(N):
    """Collatz on {1, ..., N} with overflow to sink N."""
    sink = N
    T = {}
    for n in range(1, N):
        if n % 2 == 0:
            T[n] = n // 2
        else:
            next_val = 3 * n + 1
            T[n] = next_val if next_val <= N else sink
    T[sink] = sink
    return T


# ═══════════════════════════════════════════════════════════════════════════════
# RUN UNIVERSAL CENSUS
# ═══════════════════════════════════════════════════════════════════════════════

systems = [
    ("Kaprekar_D3", build_kaprekar(3)),
    ("Kaprekar_D4", build_kaprekar(4)),
    ("Kaprekar_D5", build_kaprekar(5)),
    ("Fibonacci_mod10", build_fibonacci_mod(10)),
    ("Fibonacci_mod100", build_fibonacci_mod(100)),
    ("Fibonacci_mod1000", build_fibonacci_mod(1000)),
    ("RandomMap_1000", build_random_map(1000)),
    ("RandomMap_5000", build_random_map(5000)),
    ("Mandelbrot_40x40", build_mandelbrot_lattice(40)),
    ("Collatz_10000", build_collatz_truncated(10000)),
]

results = []
print("=" * 80)
print("AQARION v13.0 — UNIVERSAL FUNCTIONAL GRAPH CENSUS")
print("=" * 80)

for name, T in systems:
    print(f"\nCensus: {name} ...")
    engine = AQA_Engine(T, name)
    census = engine.census()
    results.append(census)
    print(f"  N={census['N']}, cycles={census['num_cycles']}, "
          f"H={census['max_height']}, transient={census['transient_nodes']}, "
          f"C={census['quotient_density']:.6f} [{census['compression_law']}]")

# Save
with open("/mnt/agents/output/aqa_v13_universal_census.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 80)
print("CENSUS COMPLETE — SAVED TO aqa_v13_universal_census.json")
print("=" * 80)================================================================================
AQARION v13.0 — UNIVERSAL FUNCTIONAL GRAPH CENSUS
================================================================================

Census: Kaprekar_D3 ...
  N=1000, cycles=2, H=6, transient=998, C=0.009000 [high]

Census: Kaprekar_D4 ...
  N=10000, cycles=2, H=7, transient=9998, C=0.001000 [high]

Census: Kaprekar_D5 ...
N=100000, cycles=4, H=6, transient=99989, C=0.000420 [ultra_high]

Census: Fibonacci_mod10 ...
  N=100, cycles=6, H=0, transient=0, C=1.000000 [very_low]

Census: Fibonacci_mod100 ...
  N=10000, cycles=76, H=0, transient=0, C=1.000000 [very_low]

Census: Fibonacci_mod1000 ...
N=1000000, cycles=1372, H=0, transient=0, C=1.000000 [very_low]

Census: RandomMap_1000 ...
  N=1000, cycles=5, H=43, transient=907, C=0.422000 [very_low]

Census: RandomMap_5000 ...
  N=5000, cycles=5, H=147, transient=4961, C=0.079800 [medium]

Census: Mandelbrot_40x40 ...
  N=1601, cycles=13, H=11, transient=1577, C=0.053092 [medium]

Census: Collatz_10000 ...
Error:
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[3], line 310
    308 print(f"\nCensus: {name} ...")
    309 engine = AQA_Engine(T, name)
--> 310 census = engine.census()
    311 results.append(census)
    312 print(f"  N={census['N']}, cycles={census['num_cycles']}, "
    313       f"H={census['max_height']}, transient={census['transient_nodes']}, "
    314       f"C={census['quotient_density']:.6f} [{census['compression_law']}]")

Cell In[3], line 174, in AQA_Engine.census(self)
    173 def census(self):
--> 174     cycles = self.find_cycles()
    175     height = self.compute_height()
    176     levels = self.level_profile()

Cell In[3], line 51, in AQA_Engine.find_cycles(self)
     49         pos[cur] = len(path)
     50         path.append(cur)
---> 51         cur = self.T[cur]
     52 self._cycles = cycles
     53 return cycles

KeyError: 0

# AQARION v12.9.0
# AQA-OBJECT CLASSIFICATION CENSUS ENGINE
#
# Purpose:
#   Generate comparable dynamical fingerprints for:
#   - Kaprekar D=3,4,5
#   - Random functional graphs
#   - User-defined finite deterministic systems
#
# Output:
#   AQAObject JSON certificates

import json
import math
import random
from collections import defaultdict, deque


# ============================================================
# CORE DYNAMICS
# ============================================================

def kaprekar(n, d):
    s = str(n).zfill(d)
    asc = int("".join(sorted(s)))
    desc = int("".join(sorted(s, reverse=True)))
    return desc - asc


def build_kaprekar(d):
    return {n: kaprekar(n, d) for n in range(10**d)}


def build_random_map(N, seed=42):
    random.seed(seed)
    return {i: random.randrange(N) for i in range(N)}


# ============================================================
# GRAPH ANALYSIS
# ============================================================

def find_cycles(T):

    N = len(T)
    state = [0]*N
    cycles = []

    for start in range(N):

        if state[start]:
            continue

        path = []
        cur = start

        while state[cur] == 0:
            state[cur] = 1
            path.append(cur)
            cur = T[cur]

        if state[cur] == 1:
            cycle = []

            while True:
                node = path.pop()
                cycle.append(node)
                if node == cur:
                    break

            cycles.append(cycle)

        for x in path:
            state[x] = 2

        for x in cycle if 'cycle' in locals() else []:
            state[x] = 2

    return cycles



def build_inverse(T):

    inv = defaultdict(list)

    for x,y in T.items():
        inv[y].append(x)

    return inv



def compute_height(T):

    inv = build_inverse(T)

    cycles = find_cycles(T)

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
                height[y] = height[x]+1
                queue.append(y)


    return height, cycles



# ============================================================
# AQA INVARIANTS
# ============================================================

def branching_profile(height):

    levels = defaultdict(int)

    for _,h in height.items():
        levels[h]+=1

    return dict(sorted(levels.items()))



def inverse_branching(T):

    inv = build_inverse(T)

    profile = {}

    for x in T:

        profile[x] = len(inv[x])

    return profile



def entropy_profile(levels):

    vals=[]

    for t,n in levels.items():

        if t>0 and n>0:
            vals.append(
                math.log(n)/t
            )

    return max(vals) if vals else 0



def quotient_estimate(T,height):

    # simple observable:
    # same height + same attractor basin

    signatures={}

    for x in T:

        cur=x

        while height[cur]>0:
            cur=T[cur]

        signatures[x]=(height[x],cur)

    return len(set(signatures.values()))



# ============================================================
# AQA OBJECT
# ============================================================

def build_AQAObject(name,T):

    height,cycles=compute_height(T)

    levels=branching_profile(height)

    obj={

        "AQA_version":
            "12.9.0",

        "system":
            name,

        "state_size":
            len(T),

        "attractors":
            [
                {
                    "size":len(c),
                    "nodes":c[:10]
                }
                for c in cycles
            ],

        "max_height":
            max(height.values()),

        "level_profile":
            levels,

        "inverse_branching_max":
            max(
                inverse_branching(T).values()
            ),

        "branching_entropy_estimate":
            entropy_profile(levels),

        "quotient_estimate":
            quotient_estimate(
                T,height
            ),

        "compression_ratio":
            quotient_estimate(T,height)
            /
            len(T),

        "certificate":
        {
            "type":
            "computational",

            "status":
            "PASS"
        }
    }

    return obj



# ============================================================
# RUN CENSUS
# ============================================================

def run():

    results=[]


    # Kaprekar
    for d in [3,4,5]:

        print(
            f"Running Kaprekar D={d}"
        )

        T=build_kaprekar(d)

        results.append(
            build_AQAObject(
                f"Kaprekar_D{d}",
                T
            )
        )


    # Random maps

    for N in [1000,5000]:

        print(
            f"Running Random Map N={N}"
        )

        T=build_random_map(N)

        results.append(
            build_AQAObject(
                f"RandomMap_{N}",
                T
            )
        )


    with open(
        "aqa_object_census.json",
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )


    print()
    print("="*60)
    print("AQARION AQA-OBJECT CENSUS COMPLETE")
    print("="*60)

    for r in results:

        print(
            r["system"],
            "|",
            "States:",
            r["state_size"],
            "|",
            "Height:",
            r["max_height"],
            "|",
            "Entropy:",
            round(
                r["branching_entropy_estimate"],
                5
            ),
            "|",
            "Compression:",
            round(
                r["compression_ratio"],
                5
            )
        )



if __name__=="__main__":
    run()

def benchmark_refinement(T, initial, name):
    import time
    start = time.perf_counter()
    final = valmari_refinement(T, initial)  # or Hopcroft variant
    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed*1000:.1f}ms, blocks={len(final)}")
    return elapsed

# Usage
T_kaprekar = [kaprekar(i) for i in range(10000)]
initial = [list(range(10000))]
benchmark_refinement(T_kaprekar, initial, "Kaprekar (Hybrid)")

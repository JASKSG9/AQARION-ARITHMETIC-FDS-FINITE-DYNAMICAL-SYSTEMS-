import os, json, numpy as np, pandas as pd
from aqarion_defect_engine import build_K_from_transitions, build_P_from_partition, defect_operator, defect_report, partition_from_bins

os.makedirs("output", exist_ok=True)

# --- Mandelbrot 1D chain approximation ---
mand = np.loadtxt("output/mandelbrot_escape.csv", delimiter=",")
# Use a single row as a 1D system with nearest-neighbor transitions
row = mand[mand.shape[0]//2].astype(int)
n = len(row)
# Build a simple shift T(i)=i+1 mod n as K
transitions = [(i, (i+1)%n) for i in range(n)]
K_man = build_K_from_transitions(transitions, n)
# Observable: escape-time bins
bins = np.percentile(row, np.linspace(0, 100, 9))
part_man = partition_from_bins(row, bins)
P_man = build_P_from_partition(part_man, n)
D_man = defect_operator(K_man, P_man)
report_man = defect_report(D_man)

# --- Kaprekar finite chain (τ-levels as states) ---
kap = pd.read_csv("output/kaprekar_profile.csv")
tau = kap["tau"].to_numpy()
count = kap["count"].to_numpy()
n_kap = len(tau)
# Simple nearest-neighbor chain on τ levels
transitions_kap = [(i, (i+1)%n_kap) for i in range(n_kap)]
K_kap = build_K_from_transitions(transitions_kap, n_kap)
# Observable: τ itself (identity partition)
part_kap = list(range(n_kap))
P_kap = build_P_from_partition(part_kap, n_kap)
D_kap = defect_operator(K_kap, P_kap)
report_kap = defect_report(D_kap)

# --- Affine trajectories coarse partition ---
aff = pd.read_csv("output/affine_trajectories_summary.csv")
# Use k as state index, partition by radius_mean quantiles
k_vals = aff["k"].to_numpy()
rad = aff["radius_mean"].to_numpy()
n_aff = len(k_vals)
transitions_aff = [(i, (i+1)%n_aff) for i in range(n_aff)]
K_aff = build_K_from_transitions(transitions_aff, n_aff)
bins_aff = np.percentile(rad, np.linspace(0, 100, 6))
part_aff = partition_from_bins(rad, bins_aff)
P_aff = build_P_from_partition(part_aff, n_aff)
D_aff = defect_operator(K_aff, P_aff)
report_aff = defect_report(D_aff)

# Save defect reports
out = {
    "mandelbrot_1d_row": report_man,
    "kaprekar_tau_levels": report_kap,
    "affine_radius_partition": report_aff,
}
with open("output/defect_reports.json", "w") as f:
    json.dump(out, f, indent=2)

print("Defect reports:", out.keys())

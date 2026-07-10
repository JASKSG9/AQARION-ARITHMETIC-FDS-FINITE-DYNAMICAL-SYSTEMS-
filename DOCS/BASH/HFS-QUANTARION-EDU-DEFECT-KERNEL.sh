from kernels import load

kernel = load("Aqarion13/aqarion-defect-kernel")

fp = kernel.compute_fingerprint(
    transition=T,
    partition=P,
)

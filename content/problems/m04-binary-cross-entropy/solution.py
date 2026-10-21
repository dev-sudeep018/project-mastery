import numpy as np

def binary_cross_entropy(y, logits):
    y, z = np.asarray(y, dtype=np.float64), np.asarray(logits, dtype=np.float64)
    if y.ndim != 1 or y.size == 0 or z.shape != y.shape:
        raise ValueError("Expected equal nonempty 1D arrays")
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(z)) or not np.all((y == 0) | (y == 1)):
        raise ValueError("Targets must be binary and logits finite")
    losses = np.maximum(z, 0) - z * y + np.log1p(np.exp(-np.abs(z)))
    return float(np.sum(losses / len(y)))

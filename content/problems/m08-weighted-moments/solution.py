import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def weighted_moments(x, weights):
    x, weights = _array(x, 1), _array(weights, 1)
    if x.size == 0 or x.shape != weights.shape or np.any(weights < 0) or weights.sum() <= 0:
        raise ValueError("Incompatible measurements or weights")
    p = weights / weights.sum()
    mean = float(p @ x)
    return {"mean": mean, "variance": float(p @ ((x - mean)**2))}

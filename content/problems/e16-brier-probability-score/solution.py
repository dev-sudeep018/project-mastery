import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def _labels(value, upper=None):
    a = _array(value, 1)
    if np.any(a < 0) or np.any(a != np.floor(a)) or (upper is not None and np.any(a >= upper)):
        raise ValueError("Labels must be nonnegative integer values within range")
    return a.astype(int)


def brier_score(labels, probabilities):
    labels, probabilities = _labels(labels,2), _array(probabilities,1)
    if labels.size == 0 or labels.shape != probabilities.shape or np.any(probabilities < 0) or np.any(probabilities > 1):
        raise ValueError("Invalid probability forecasts")
    return float(np.mean((probabilities-labels)**2))

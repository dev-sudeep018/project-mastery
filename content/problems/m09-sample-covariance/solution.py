import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def sample_covariance(X):
    X = _array(X, 2)
    if X.shape[0] < 2 or X.shape[1] < 1:
        raise ValueError("Need at least two observations and one feature")
    centered = X - X.mean(axis=0)
    return centered.T @ centered / (len(X) - 1)

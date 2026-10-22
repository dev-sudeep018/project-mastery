import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def pairwise_squared_distances(X, Y):
    X, Y = _array(X, 2), _array(Y, 2)
    if min(X.shape + Y.shape) < 1 or X.shape[1] != Y.shape[1]:
        raise ValueError("Need nonempty matrices with matching features")
    return np.sum((X[:, None, :] - Y[None, :, :])**2, axis=-1)

import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def project_reconstruct(X, mean, components):
    X, mean, components = _array(X, 2), _array(mean, 1), _array(components, 2)
    n, d = X.shape
    k = len(components)
    if n < 1 or d < 1 or mean.shape != (d,) or components.shape[1] != d or not 1 <= k <= d:
        raise ValueError("Incompatible projection shapes")
    if not np.allclose(components @ components.T, np.eye(k), atol=1e-7, rtol=0):
        raise ValueError("Components must be orthonormal")
    scores = (X-mean) @ components.T
    return {"scores":scores, "reconstruction":scores @ components + mean}

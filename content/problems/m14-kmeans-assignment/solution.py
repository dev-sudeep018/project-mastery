import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def assign_clusters(X, centers):
    X, centers = _array(X, 2), _array(centers, 2)
    if min(X.shape + centers.shape) < 1 or X.shape[1] != centers.shape[1]:
        raise ValueError("Incompatible observations and centers")
    distances = np.sum((X[:, None, :] - centers[None, :, :])**2, axis=2)
    return {"labels": np.argmin(distances, axis=1), "inertia": float(distances.min(axis=1).sum())}

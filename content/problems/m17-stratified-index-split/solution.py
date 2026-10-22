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


def stratified_indices(labels, train_fraction):
    labels = _labels(labels)
    if labels.size == 0 or not np.isfinite(train_fraction) or not 0 < train_fraction < 1:
        raise ValueError("Invalid labels or split fraction")
    train, test = [], []
    for label in np.unique(labels):
        indices = np.flatnonzero(labels == label).tolist()
        if len(indices) < 2:
            raise ValueError("Every class needs two rows")
        count = min(len(indices)-1, max(1, int(np.floor(len(indices)*train_fraction))))
        train.extend(indices[:count]); test.extend(indices[count:])
    return {"train":sorted(train), "test":sorted(test)}

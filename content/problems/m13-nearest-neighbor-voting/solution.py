import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def _integer(value, minimum=1):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError("Expected an integer in the allowed range")
    return int(value)


def _labels(value, upper=None):
    a = _array(value, 1)
    if np.any(a < 0) or np.any(a != np.floor(a)) or (upper is not None and np.any(a >= upper)):
        raise ValueError("Labels must be nonnegative integer values within range")
    return a.astype(int)


def knn_predict(train, labels, queries, k):
    train, queries = _array(train, 2), _array(queries, 2)
    labels, k = _labels(labels), _integer(k)
    if min(train.shape + queries.shape) < 1 or train.shape[1] != queries.shape[1] or len(labels) != len(train) or k > len(train):
        raise ValueError("Incompatible training set, queries, or k")
    predictions = []
    for q in queries:
        nearest = np.argsort(np.sum((train-q)**2, axis=1), kind="stable")[:k]
        values, counts = np.unique(labels[nearest], return_counts=True)
        predictions.append(values[np.argmax(counts)])
    return np.array(predictions)

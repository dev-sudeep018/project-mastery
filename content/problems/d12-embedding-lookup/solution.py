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


def embedding_lookup(table, token_ids):
    table = _array(table, 2)
    token_ids = _labels(token_ids, len(table))
    if min(table.shape) < 1 or token_ids.size == 0:
        raise ValueError("Need a table and token IDs")
    return table[token_ids].copy()

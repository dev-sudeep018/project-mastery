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


def embedding_gradient(token_ids, upstream, vocab_size):
    vocab_size = _integer(vocab_size)
    token_ids, upstream = _labels(token_ids, vocab_size), _array(upstream, 2)
    if token_ids.size == 0 or len(upstream) != len(token_ids) or upstream.shape[1] < 1:
        raise ValueError("Incompatible token gradients")
    gradient = np.zeros((vocab_size, upstream.shape[1]))
    np.add.at(gradient, token_ids, upstream)
    return gradient

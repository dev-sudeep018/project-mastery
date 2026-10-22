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


def causal_padding_mask(lengths, max_length):
    max_length = _integer(max_length)
    lengths = _labels(lengths, max_length+1)
    if lengths.size == 0:
        raise ValueError("Need at least one sequence")
    p = np.arange(max_length)
    valid = p[None,:] < lengths[:,None]
    return (p[None,:] <= p[:,None])[None,:,:] & valid[:,:,None] & valid[:,None,:]

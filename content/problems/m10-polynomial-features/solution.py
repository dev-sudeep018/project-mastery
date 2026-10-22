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


def polynomial_features(x, degree):
    x = _array(x, 1)
    degree = _integer(degree)
    if x.size == 0 or degree > 5:
        raise ValueError("Empty input or unsupported degree")
    return x[:, None] ** np.arange(degree + 1)

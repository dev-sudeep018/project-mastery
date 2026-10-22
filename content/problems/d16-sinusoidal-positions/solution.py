import numpy as np


def _integer(value, minimum=1):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError("Expected an integer in the allowed range")
    return int(value)


def sinusoidal_positions(length, dimensions):
    length, dimensions = _integer(length), _integer(dimensions)
    if dimensions % 2:
        raise ValueError("Dimensions must be even")
    angles = np.arange(length)[:,None] * 10000.**(-np.arange(0,dimensions,2)/dimensions)
    out = np.empty((length, dimensions))
    out[:,0::2], out[:,1::2] = np.sin(angles), np.cos(angles)
    return out

import numpy as np


def softmax(x):
    """Stable softmax for nonempty finite 1D numeric inputs."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("Expected a nonempty, finite 1D array")
    # Extreme finite differences can underflow to -inf; exp(-inf) = 0
    # is the correct limiting probability for the smaller score.
    with np.errstate(over="ignore", under="ignore"):
        shifted = x - np.max(x)
        weights = np.exp(shifted)
    return weights / np.sum(weights)

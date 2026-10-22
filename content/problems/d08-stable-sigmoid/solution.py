import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def sigmoid_with_gradient(x):
    x = _array(x, 1)
    if x.size == 0:
        raise ValueError("Need a nonempty vector")
    output = np.empty_like(x)
    positive = x >= 0
    output[positive] = 1 / (1 + np.exp(-x[positive]))
    exp_x = np.exp(x[~positive])
    output[~positive] = exp_x / (1 + exp_x)
    return {"output":output, "derivative":output*(1-output)}

import numpy as np

def inverted_dropout(x, keep, p, training):
    x, keep, p = np.asarray(x, dtype=np.float64), np.asarray(keep), np.asarray(p, dtype=np.float64)
    if x.ndim == 0 or x.size == 0 or keep.shape != x.shape or keep.dtype != np.bool_:
        raise ValueError("Expected a nonempty array and equal boolean mask")
    if type(training) is not bool or p.ndim != 0 or not np.isfinite(p) or not 0 <= p < 1 or not np.all(np.isfinite(x)):
        raise ValueError("Invalid training flag, probability, or activation")
    return x * keep / (1-p) if training else x.copy()

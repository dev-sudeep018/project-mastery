import numpy as np

def relu_backward(x, upstream):
    x, upstream = [np.asarray(a, dtype=np.float64) for a in (x, upstream)]
    if x.ndim == 0 or x.size == 0 or upstream.shape != x.shape:
        raise ValueError("Expected equal nonempty array shapes")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(upstream)):
        raise ValueError("Inputs must be finite")
    return {"output": np.maximum(x, 0), "dx": upstream * (x > 0)}

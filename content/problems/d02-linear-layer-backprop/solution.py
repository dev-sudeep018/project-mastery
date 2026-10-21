import numpy as np

def linear_backward(X, W, grad_output):
    X, W, G = [np.asarray(v, dtype=np.float64) for v in (X, W, grad_output)]
    if any(v.ndim != 2 or min(v.shape) == 0 for v in (X,W,G)):
        raise ValueError("Expected nonempty matrices")
    if X.shape[1] != W.shape[0] or G.shape != (X.shape[0], W.shape[1]):
        raise ValueError("Incompatible shapes")
    if not all(np.all(np.isfinite(v)) for v in (X,W,G)):
        raise ValueError("Inputs must be finite")
    return {"dx": G @ W.T, "dw": X.T @ G, "db": G.sum(axis=0)}

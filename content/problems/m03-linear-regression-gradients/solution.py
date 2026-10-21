import numpy as np

def linear_gradients(X, y, w, b):
    X, y, w = [np.asarray(v, dtype=np.float64) for v in (X, y, w)]
    if X.ndim != 2 or min(X.shape) == 0 or y.shape != (X.shape[0],) or w.shape != (X.shape[1],):
        raise ValueError("Incompatible nonempty X, y, and w shapes")
    b = np.asarray(b, dtype=np.float64)
    if b.ndim != 0 or not all(np.all(np.isfinite(v)) for v in (X, y, w, b)):
        raise ValueError("Inputs must be finite and b must be a scalar")
    residual = X @ w + float(b) - y
    return {"loss": float(np.mean(residual ** 2) / 2), "dw": X.T @ residual / X.shape[0], "db": float(np.mean(residual))}

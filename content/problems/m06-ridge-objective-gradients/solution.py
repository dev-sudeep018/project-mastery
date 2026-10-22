import numpy as np

def ridge_gradients(X, y, w, b, strength):
    X, y, w, b, strength = [np.asarray(a, dtype=np.float64) for a in (X, y, w, b, strength)]
    if X.ndim != 2 or min(X.shape) == 0 or y.shape != (X.shape[0],) or w.shape != (X.shape[1],):
        raise ValueError("Incompatible nonempty regression shapes")
    if b.ndim != 0 or strength.ndim != 0 or strength < 0 or not all(np.all(np.isfinite(a)) for a in (X,y,w,b,strength)):
        raise ValueError("Expected finite inputs and nonnegative scalar strength")
    residual = X @ w + b - y
    return {"loss": float(np.mean(residual**2)/2 + strength*np.sum(w**2)/2),
            "dw": X.T @ residual / len(X) + strength*w, "db": float(residual.mean())}

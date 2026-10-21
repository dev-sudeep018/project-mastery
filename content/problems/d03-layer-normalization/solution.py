import numpy as np

def layer_norm(X, gamma, beta, eps=1e-5):
    X, gamma, beta, eps = [np.asarray(v, dtype=np.float64) for v in (X,gamma,beta,eps)]
    if X.ndim not in (1,2) or X.size == 0 or gamma.shape != (X.shape[-1],) or beta.shape != gamma.shape:
        raise ValueError("Incompatible nonempty feature shapes")
    if eps.ndim != 0 or eps <= 0 or not all(np.all(np.isfinite(v)) for v in (X,gamma,beta,eps)):
        raise ValueError("Expected finite inputs and positive scalar eps")
    centered = X - X.mean(axis=-1, keepdims=True)
    return centered / np.sqrt(np.mean(centered**2, axis=-1, keepdims=True) + eps) * gamma + beta

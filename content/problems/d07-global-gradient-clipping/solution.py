import numpy as np

def clip_gradients(grads, max_norm):
    if not isinstance(grads, list) or not grads:
        raise ValueError("Expected a nonempty list of gradients")
    arrays = [np.asarray(a, dtype=np.float64) for a in grads]
    limit = np.asarray(max_norm, dtype=np.float64)
    if limit.ndim != 0 or not np.isfinite(limit) or limit < 0 or any(a.ndim == 0 or a.size == 0 or not np.all(np.isfinite(a)) for a in arrays):
        raise ValueError("Expected finite nonempty arrays and nonnegative scalar limit")
    norm = float(np.sqrt(sum(np.sum(a*a) for a in arrays)))
    factor = min(1., float(limit)/norm) if norm else 1.
    return {"norm": norm, "grads": [a*factor for a in arrays]}

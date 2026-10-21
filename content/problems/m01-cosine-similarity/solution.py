import numpy as np

def cosine_similarity(a, b):
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    if a.ndim != 1 or b.ndim != 1 or a.size == 0 or a.shape != b.shape:
        raise ValueError("Expected nonempty vectors of equal length")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("Vectors must be finite")
    sa, sb = np.max(np.abs(a)), np.max(np.abs(b))
    if sa == 0 or sb == 0:
        return 0.0
    a, b = a / sa, b / sb
    a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
    return float(np.clip(np.dot(a, b), -1.0, 1.0))

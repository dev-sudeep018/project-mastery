import numpy as np

def tfidf_weights(counts):
    counts = np.asarray(counts, dtype=np.float64)
    if counts.ndim != 2 or min(counts.shape) == 0 or not np.all(np.isfinite(counts)) or np.any(counts < 0) or np.any(counts != np.floor(counts)):
        raise ValueError("Expected a nonempty nonnegative integer count matrix")
    idf = np.log((1 + len(counts)) / (1 + np.sum(counts > 0, axis=0))) + 1
    weighted = counts * idf
    lengths = np.linalg.norm(weighted, axis=1, keepdims=True)
    weights = np.divide(weighted, lengths, out=np.zeros_like(weighted), where=lengths > 0)
    return {"idf": idf, "weights": weights}

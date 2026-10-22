import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def bm25_scores(counts, query, k1, b):
    counts, query = _array(counts, 2), _array(query, 1)
    if min(counts.shape) < 1 or len(query) != counts.shape[1] or np.any(counts < 0) or np.any(counts != np.floor(counts)) or np.any(query < 0) or np.any(query != np.floor(query)):
        raise ValueError("Invalid count representation")
    if not np.isfinite(k1) or k1 <= 0 or not np.isfinite(b) or not 0 <= b <= 1:
        raise ValueError("Invalid BM25 parameters")
    lengths = counts.sum(axis=1)
    average = lengths.mean()
    if average == 0:
        return np.zeros(len(counts))
    df = (counts > 0).sum(axis=0)
    idf = np.log(1+(len(counts)-df+.5)/(df+.5))
    denominator = counts + k1*(1-b+b*lengths[:,None]/average)
    saturation = np.divide(counts*(k1+1), denominator, out=np.zeros_like(counts), where=denominator > 0)
    return (saturation*idf) @ query

import numpy as np

def masked_attention(Q, K, V, mask):
    Q,K,V = [np.asarray(v,dtype=np.float64) for v in (Q,K,V)]
    mask = np.asarray(mask)
    if any(a.ndim != 2 or min(a.shape) == 0 for a in (Q,K,V)):
        raise ValueError("Expected nonempty matrices")
    if Q.shape[1] != K.shape[1] or K.shape[0] != V.shape[0] or mask.shape != (Q.shape[0],K.shape[0]) or mask.dtype != np.bool_:
        raise ValueError("Incompatible matrices or boolean mask")
    if not all(np.all(np.isfinite(a)) for a in (Q,K,V)):
        raise ValueError("Inputs must be finite")
    scores = np.where(mask, Q @ K.T / np.sqrt(Q.shape[1]), -np.inf)
    maximum = np.where(mask.any(axis=1,keepdims=True), scores.max(axis=1,keepdims=True), 0)
    numerator = np.exp(scores-maximum)
    denominator = numerator.sum(axis=1,keepdims=True)
    weights = np.divide(numerator,denominator,out=np.zeros_like(numerator),where=denominator>0)
    return {"weights":weights, "output":weights @ V}

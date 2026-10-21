import numpy as np

def top_k_cosine(query, vectors, k):
    q, v = np.asarray(query,dtype=np.float64), np.asarray(vectors,dtype=np.float64)
    if q.ndim != 1 or q.size == 0 or v.ndim != 2 or v.shape[0] == 0 or v.shape[1] != q.size:
        raise ValueError("Incompatible nonempty vectors")
    if type(k) is not int or not 0 <= k <= v.shape[0] or not np.all(np.isfinite(q)) or not np.all(np.isfinite(v)):
        raise ValueError("Invalid k or non-finite vector")
    def normalize(a):
        scale = np.max(np.abs(a),axis=-1,keepdims=True)
        a = np.divide(a,scale,out=np.zeros_like(a),where=scale>0)
        length = np.linalg.norm(a,axis=-1,keepdims=True)
        return np.divide(a,length,out=np.zeros_like(a),where=length>0)
    scores = normalize(v) @ normalize(q)
    return np.lexsort((np.arange(len(v)),-scores))[:k].tolist()

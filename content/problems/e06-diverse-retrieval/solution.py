import numpy as np

def mmr_select(relevance, similarity, k, weight):
    relevance, similarity, weight = [np.asarray(a, dtype=np.float64) for a in (relevance, similarity, weight)]
    if relevance.ndim != 1 or relevance.size == 0 or similarity.shape != (relevance.size, relevance.size):
        raise ValueError("Expected relevance vector and matching similarity matrix")
    if type(k) is not int or not 0 <= k <= len(relevance) or weight.ndim != 0 or not np.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError("Invalid cutoff or relevance weight")
    if any(not np.all(np.isfinite(a)) or np.any((a < 0) | (a > 1)) for a in (relevance, similarity)) or not np.allclose(similarity, similarity.T, atol=1e-8, rtol=0) or not np.allclose(np.diag(similarity), 1, atol=1e-8, rtol=0):
        raise ValueError("Invalid relevance or similarity scores")
    selected = []
    while len(selected) < k:
        candidates = [i for i in range(len(relevance)) if i not in selected]
        def score(i):
            return float(weight*relevance[i] - (1-weight)*np.max(similarity[i, selected])) if selected else float(relevance[i])
        selected.append(max(candidates, key=score))
    return selected

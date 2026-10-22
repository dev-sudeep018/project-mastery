import numpy as np

def binary_metrics(y, scores, threshold):
    y, scores, threshold = [np.asarray(a, dtype=np.float64) for a in (y, scores, threshold)]
    if y.ndim != 1 or y.size == 0 or scores.shape != y.shape or threshold.ndim != 0:
        raise ValueError("Expected matching nonempty vectors and scalar threshold")
    if not all(np.all(np.isfinite(a)) for a in (y,scores,threshold)) or not np.all((y == 0) | (y == 1)) or np.any((scores < 0) | (scores > 1)) or not 0 <= threshold <= 1:
        raise ValueError("Invalid binary labels or probability range")
    positive, predicted = y == 1, scores >= threshold
    tp, fp = int(np.sum(predicted & positive)), int(np.sum(predicted & ~positive))
    tn, fn = int(np.sum(~predicted & ~positive)), int(np.sum(~predicted & positive))
    return {"tp":tp, "fp":fp, "tn":tn, "fn":fn,
            "precision":tp/(tp+fp) if tp+fp else 0.,
            "recall":tp/(tp+fn) if tp+fn else 0.,
            "f1":2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.}

import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def _labels(value, upper=None):
    a = _array(value, 1)
    if np.any(a < 0) or np.any(a != np.floor(a)) or (upper is not None and np.any(a >= upper)):
        raise ValueError("Labels must be nonnegative integer values within range")
    return a.astype(int)


def pairwise_auc(labels, scores):
    labels, scores = _labels(labels,2), _array(scores,1)
    if labels.shape != scores.shape or not np.any(labels == 0) or not np.any(labels == 1):
        raise ValueError("Need paired scores with both classes")
    positive, negative = scores[labels==1][:,None], scores[labels==0][None,:]
    return float(np.mean(positive > negative)+.5*np.mean(positive == negative))

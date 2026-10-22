import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def _integer(value, minimum=1):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError("Expected an integer in the allowed range")
    return int(value)


def _labels(value, upper=None):
    a = _array(value, 1)
    if np.any(a < 0) or np.any(a != np.floor(a)) or (upper is not None and np.any(a >= upper)):
        raise ValueError("Labels must be nonnegative integer values within range")
    return a.astype(int)


def calibration_bins(labels, probabilities, num_bins):
    labels, probabilities = _labels(labels,2), _array(probabilities,1)
    num_bins = _integer(num_bins)
    if labels.size == 0 or labels.shape != probabilities.shape or np.any(probabilities < 0) or np.any(probabilities > 1):
        raise ValueError("Invalid probability forecasts")
    indices = np.minimum((probabilities*num_bins).astype(int),num_bins-1)
    counts = np.bincount(indices,minlength=num_bins)
    sums = np.bincount(indices,weights=probabilities,minlength=num_bins)
    positives = np.bincount(indices,weights=labels,minlength=num_bins)
    means = np.divide(sums,counts,out=np.zeros(num_bins),where=counts>0)
    fractions = np.divide(positives,counts,out=np.zeros(num_bins),where=counts>0)
    return {"counts":counts,"mean_probability":means,"positive_fraction":fractions,"ece":float(counts @ np.abs(means-fractions)/len(labels))}

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


def confusion_matrix(actual, predicted, num_classes):
    num_classes = _integer(num_classes)
    actual, predicted = _labels(actual,num_classes), _labels(predicted,num_classes)
    if actual.size == 0 or actual.shape != predicted.shape:
        raise ValueError("Need paired nonempty labels")
    result = np.zeros((num_classes,num_classes),dtype=int)
    np.add.at(result,(actual,predicted),1)
    return result

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


def select_context(costs, scores, budget):
    costs, scores = _labels(costs), _array(scores, 1)
    budget = _integer(budget, 0)
    if costs.size == 0 or costs.shape != scores.shape or np.any(costs == 0) or np.any(scores < 0):
        raise ValueError("Invalid candidate costs or scores")
    selected = []
    for i in sorted(range(len(costs)),key=lambda i:(-scores[i],i)):
        if costs[i] <= budget:
            selected.append(i); budget -= int(costs[i])
    return selected

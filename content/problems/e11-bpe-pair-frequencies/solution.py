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


def bpe_pair_counts(words, frequencies):
    if not isinstance(words,list) or not words or any(not isinstance(w,list) or any(not isinstance(t,str) or not t for t in w) for w in words):
        raise ValueError("Expected segmented words")
    frequencies = _labels(frequencies)
    if len(frequencies) != len(words):
        raise ValueError("Need one frequency per word")
    result = {}
    for word,frequency in zip(words,frequencies):
        if frequency:
            for pair in zip(word,word[1:]):
                result[pair] = result.get(pair,0) + int(frequency)
    return result

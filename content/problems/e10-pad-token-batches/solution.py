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


def pad_token_batch(sequences, pad_id):
    pad_id = _integer(pad_id, 0)
    if not isinstance(sequences,list) or not sequences or any(not isinstance(s,list) for s in sequences):
        raise ValueError("Expected a nonempty list of token lists")
    rows = [_labels(s) for s in sequences]
    width = max(map(len,rows))
    tokens = np.full((len(rows),width),pad_id,dtype=int)
    mask = np.zeros(tokens.shape,dtype=bool)
    for i,row in enumerate(rows):
        tokens[i,:len(row)], mask[i,:len(row)] = row, True
    return {"tokens":tokens,"mask":mask}

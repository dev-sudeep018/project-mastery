import numpy as np

def standardize_split(train, test):
    train, test = [np.asarray(a, dtype=np.float64) for a in (train, test)]
    if train.ndim != 2 or test.ndim != 2 or min(train.shape) == 0 or test.shape[1] != train.shape[1]:
        raise ValueError("Expected nonempty training axes and matching test features")
    if not np.all(np.isfinite(train)) or not np.all(np.isfinite(test)):
        raise ValueError("Features must be finite")
    mean = train.mean(axis=0)
    scale = train.std(axis=0, ddof=0)
    scale = np.where(scale == 0, 1.0, scale)
    return {"mean": mean, "scale": scale, "train": (train-mean)/scale, "test": (test-mean)/scale}

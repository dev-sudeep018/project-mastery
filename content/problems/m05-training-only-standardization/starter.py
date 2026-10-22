import numpy as np

def standardize_split(train, test):
    """Investigate this intentionally flawed scaler, then repair its contract."""
    train, test = [np.asarray(a, dtype=np.float64) for a in (train, test)]
    combined = np.vstack([train, test])  # Which rows may fit this transform?
    mean = combined.mean(axis=0)
    scale = combined.std(axis=0)
    return {"mean": mean, "scale": scale, "train": (train-mean)/scale, "test": (test-mean)/scale}

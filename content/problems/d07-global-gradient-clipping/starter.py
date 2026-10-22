import numpy as np

def clip_gradients(grads, max_norm):
    """This intentionally flawed patch clips coordinates. Repair its geometry."""
    arrays = [np.asarray(a, dtype=np.float64) for a in grads]
    norm = float(np.sqrt(sum(np.sum(a*a) for a in arrays)))
    return {"norm": norm, "grads": [np.clip(a, -max_norm, max_norm) for a in arrays]}

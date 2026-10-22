import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def momentum_step(parameters, gradient, velocity, learning_rate, beta):
    parameters, gradient, velocity = [_array(a, 1) for a in (parameters,gradient,velocity)]
    if parameters.size == 0 or parameters.shape != gradient.shape or parameters.shape != velocity.shape or not np.isfinite(learning_rate) or learning_rate <= 0 or not np.isfinite(beta) or not 0 <= beta < 1:
        raise ValueError("Invalid optimizer state")
    updated = beta*velocity + gradient
    return {"parameters":parameters-learning_rate*updated, "velocity":updated}

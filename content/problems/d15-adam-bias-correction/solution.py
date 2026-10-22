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


def adam_step(parameters, gradient, m, v, t, learning_rate, beta1, beta2, epsilon):
    parameters, gradient, m, v = [_array(a, 1) for a in (parameters,gradient,m,v)]
    t = _integer(t)
    if parameters.size == 0 or any(a.shape != parameters.shape for a in (gradient,m,v)) or np.any(v < 0):
        raise ValueError("Invalid moment shapes or values")
    if not all(np.isfinite(a) for a in (learning_rate,beta1,beta2,epsilon)) or learning_rate <= 0 or epsilon <= 0 or not 0 <= beta1 < 1 or not 0 <= beta2 < 1:
        raise ValueError("Invalid optimizer hyperparameters")
    new_m = beta1*m + (1-beta1)*gradient
    new_v = beta2*v + (1-beta2)*gradient**2
    update = (new_m/(1-beta1**t)) / (np.sqrt(new_v/(1-beta2**t))+epsilon)
    return {"parameters":parameters-learning_rate*update, "m":new_m, "v":new_v}

import numpy as np

def numerical_derivative(f, x, h=1e-5):
    def scalar(value):
        a = np.asarray(value, dtype=np.float64)
        if a.ndim != 0 or not np.isfinite(a):
            raise ValueError("Expected a finite scalar")
        return float(a)
    if not callable(f):
        raise ValueError("f must be callable")
    x, h = scalar(x), scalar(h)
    if h <= 0 or not np.isfinite(x+h) or not np.isfinite(x-h) or x+h == x or x-h == x:
        raise ValueError("Step must be positive and representable")
    return (scalar(f(x+h)) - scalar(f(x-h))) / (2*h)

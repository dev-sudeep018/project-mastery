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


def max_pool(image, window, stride):
    image = _array(image, 2)
    stride = _integer(stride)
    if not isinstance(window, (tuple,list)) or len(window) != 2:
        raise ValueError("Need a two-axis window")
    h, w = [_integer(v) for v in window]
    if min(image.shape) < 1 or h > image.shape[0] or w > image.shape[1]:
        raise ValueError("Window must fit")
    out = np.empty(((image.shape[0]-h)//stride+1, (image.shape[1]-w)//stride+1))
    for i,j in np.ndindex(out.shape):
        out[i,j] = image[i*stride:i*stride+h,j*stride:j*stride+w].max()
    return out

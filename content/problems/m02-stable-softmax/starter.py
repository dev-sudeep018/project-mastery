import numpy as np


def softmax(x):
    """Convert a finite 1D array of scores to probabilities.

    Raise ValueError for empty, non-finite, or non-1D input.
    Do not modify the input array.
    """
    x = np.asarray(x, dtype=np.float64)

    # 1. Validate the input.
    # 2. Shift the scores before exponentiating.
    # 3. Normalize so the probabilities sum to 1.
    raise NotImplementedError("Your implementation goes here")

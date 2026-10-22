import numpy as np


def _array(value, rank):
    a = np.asarray(value, dtype=float)
    if a.ndim != rank or not np.all(np.isfinite(a)):
        raise ValueError("Expected a finite numeric array of the specified rank")
    return a


def gaussian_log_joint(X, priors, means, variances):
    X, priors = _array(X, 2), _array(priors, 1)
    means, variances = _array(means, 2), _array(variances, 2)
    if min(X.shape + means.shape) < 1 or means.shape != variances.shape or means.shape[1] != X.shape[1] or len(priors) != len(means) or np.any(priors <= 0) or abs(priors.sum()-1) > 1e-7 or np.any(variances <= 0):
        raise ValueError("Invalid Gaussian parameters")
    scores = np.log(priors)[None,:] - .5*np.sum(np.log(2*np.pi*variances)[None,:,:] + (X[:,None,:]-means[None,:,:])**2/variances[None,:,:], axis=2)
    return {"log_joint":scores, "predictions":np.argmax(scores,axis=1)}

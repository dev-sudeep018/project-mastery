# Add Regularization to Linear Regression

The data term rewards predictions that match targets. The second term charges for large weights, so even a perfect fit can have a nonzero objective and gradient.

For the stated convention, dw = X.T @ residual / n + strength\*w, while db = mean(residual). The intercept does not appear in the penalty.

Penalty constants depend on whether a library sums or averages its data loss. Compare the full objective before transferring a strength value between implementations.

Experiment with a perfect fit and increase strength. Explain why a gradient step can temporarily increase training error while decreasing the regularized objective. Scale features using training statistics before comparing the cost of their coefficients.

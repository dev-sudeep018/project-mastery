# Numerical Differentiation

Central differences approximate the tangent using a symmetric secant. For a smooth function, the leading truncation error is proportional to h².

A gradient check is a diagnostic, not a training algorithm: evaluating every parameter twice is expensive.

An inaccurate numerical derivative does not automatically prove the analytic gradient wrong. Check step size, precision, and whether the function is differentiable there.

## Contract

- Use (f(x+h) - f(x-h)) / (2\*h).
- Require a callable f, finite scalar x, and positive finite scalar h. Reject invalid inputs with ValueError.
- Reject steps that round x+h or x-h back to x, or produce non-finite sample points.
- Require both function evaluations to be finite numeric scalars. This exercise uses smooth functions.

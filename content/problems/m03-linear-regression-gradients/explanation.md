# Linear Regression Gradients

Each residual contributes to the gradient. Matrix multiplication X.T @ residual adds all feature-weighted residuals in one operation.

Because the loss averages over examples, its gradient must average too. Using a sum instead changes the effective step size whenever the batch size changes.

The derivative of a prediction with respect to b is one, so db is simply the mean residual. These gradients can be checked independently by finite differences.

## Contract

- X has shape (n, d), y has shape (n,), w has shape (d,), and b is a finite scalar.
- Require n >= 1 and d >= 1. Reject non-finite values and incompatible shapes with ValueError.
- Return dw as a NumPy array and loss/db as numeric scalars. Average gradients over the batch.
- Do not modify any input. Evaluation uses moderate finite values.

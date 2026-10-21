# Backpropagation through a Linear Layer

The vector-Jacobian product avoids constructing a large Jacobian explicitly. Matrix multiplication performs the same chain-rule accumulation.

dx = G @ W.T, dw = X.T @ G, and db = sum(G, axis=0). Each expression can be checked by its shape.

The batch reduction belongs to the loss definition. Adding a second division by n here would silently shrink every upstream gradient.

## Contract

- X has shape (n,d), W has shape (d,o), and grad_output has shape (n,o). All dimensions must be positive.
- Return NumPy arrays: dx (n,d), dw (d,o), and db (o,).
- Sum bias and weight contributions over the batch. Do not introduce an additional average.
- Accept numeric lists or arrays. Reject incompatible, non-finite, or non-2D inputs with ValueError; leave inputs unchanged.

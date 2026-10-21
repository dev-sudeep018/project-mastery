# Masked Scaled Dot-Product Attention

The dot products measure query-key compatibility. Scaling by the square root of the key dimension moderates their growth as the dimension increases.

Masking happens before normalization. Zeroing probabilities afterward would leave valid rows with weights that no longer sum to one.

An entirely masked row has no probability distribution. This exercise defines a zero result so downstream code gets an explicit, finite outcome.

## Contract

- Q has shape (m,d), K (n,d), V (n,v), and boolean mask (m,n), with positive dimensions.
- Scale scores by sqrt(d), apply the mask, and use a numerically stable softmax per row.
- An entirely masked row must have zero weights and zero output.
- Reject incompatible shapes, non-boolean masks, or non-finite inputs with ValueError. Do not mutate inputs; test dot products are representable.

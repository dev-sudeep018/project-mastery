# Top-K Vector Retrieval

Cosine ranking depends on direction, not vector length. A longer embedding is not automatically a more relevant document.

Tie-breaking is part of the contract: deterministic results make evaluation and debugging reproducible.

This exact scan is a baseline for small corpora. Approximate indexes become useful at larger scales, where latency and recall trade off.

## Contract

- query is a nonempty 1D vector; vectors is a nonempty 2D matrix with the same feature count.
- k is an integer between 0 and the number of rows, inclusive; booleans are invalid.
- Define similarity as zero whenever either vector is zero. Handle large and tiny finite vectors safely.
- Reject invalid shapes, non-finite values, or invalid k with ValueError. Leave all inputs unchanged.

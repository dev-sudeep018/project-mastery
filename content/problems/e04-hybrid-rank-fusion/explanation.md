# Hybrid Rank Fusion

Reciprocal rank fusion uses positions rather than raw retrieval scores. This avoids pretending that cosine and keyword scores share a scale.

The rank constant controls how sharply early positions dominate. Larger values flatten the differences among nearby ranks.

Fusion is a hypothesis to evaluate, not a guaranteed improvement. Compare against each baseline on held-out queries and inspect individual misses.

## Contract

- rankings is a list of lists of string IDs. Deduplicate each list in order before assigning one-based ranks.
- rank_constant must be a positive finite numeric scalar, excluding booleans. Default weights are all 1.
- Optional weights must match the number of lists, be finite and nonnegative, and contain a positive value unless there are no lists.
- Break score ties by ascending document ID. limit is None or a nonnegative integer (not bool); larger limits simply return every document. Leave inputs unchanged and raise ValueError for invalid inputs.

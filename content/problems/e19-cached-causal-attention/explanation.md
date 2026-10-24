# Reuse Keys and Values during Causal Decoding

Caching avoids recomputing past projected keys and values in a full model, but the current query still compares against the growing history. This small NumPy exercise demonstrates correctness rather than optimized memory or runtime.

An unshifted triangular mask fails as soon as a cache exists. Omitting a mask for multi-token chunks leaks information from future tokens in that chunk.

Adapted the upstream cache concatenation and shifted causal mask. Removed learned projections, multiple heads and autograd so the cache state transition is directly inspectable.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/kv_cache.py

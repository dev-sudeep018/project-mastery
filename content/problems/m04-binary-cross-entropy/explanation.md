# Binary Cross-Entropy from Logits

The logit is a raw score. A sigmoid would turn it into a probability, but computing that probability first can round to exactly zero or one.

The stable logits expression combines the sigmoid and logarithm algebraically. log1p retains precision when the exponential is very small.

This loss measures prediction quality, not classification accuracy. Two models can make the same binary decisions but express very different confidence.

## Contract

- Both inputs are nonempty finite one-dimensional arrays of the same shape; lists are accepted.
- Every target must equal 0 or 1. Raise ValueError for invalid targets, shapes, or non-finite inputs.
- Return a finite numeric scalar and do not mutate inputs.
- Compute from logits, not probabilities. Large correct predictions approach zero loss.

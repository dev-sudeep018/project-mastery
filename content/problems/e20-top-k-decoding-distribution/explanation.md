# Inspect a Truncated Decoding Distribution

Temperature changes relative probabilities within the retained set. It does not change the ranking when positive, and k=1 always produces a one-hot distribution.

A smaller candidate set can remove plausible tokens. Returning the whole probability vector lets you see that tradeoff without interpreting individual random draws.

Adapted the upstream top-k and temperature steps while removing top-p filtering and random sampling. Unlike its threshold-based tie handling, this contract retains exactly k indices with stable index-order ties.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/topk_sampling.py

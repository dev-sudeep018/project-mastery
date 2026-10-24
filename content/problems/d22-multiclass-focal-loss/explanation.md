# Reduce Easy-Example Contributions with Focal Loss

At gamma zero, the focusing factor is one and the loss is scalar-alpha-weighted cross-entropy. Larger gamma downweights easy examples more strongly, without proving better model performance.

The upstream implementation adds 1e-8 before taking the logarithm. This adaptation uses log-softmax instead, avoiding the artificial loss cap on extreme wrong predictions.

This exercise ports the upstream forward objective to NumPy. It adds explicit validation, deterministic edge cases and the gamma-zero limit; it does not provide automatic gradients.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/focal_loss.py

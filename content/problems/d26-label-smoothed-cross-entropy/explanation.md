# Distribute Target Mass with Label Smoothing

At smoothing zero the objective is ordinary multiclass cross-entropy. At smoothing one the originally correct class receives no mass; that boundary defines the formula rather than recommending a training choice.

The smoothing convention must be specified when comparing implementations. Assigning smoothing/C everywhere produces a different target and a different loss.

Ported the upstream non-target-only target distribution and stable log-softmax to NumPy. Added strict label/range validation and original fixtures.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/label_smoothing.py

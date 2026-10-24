# Normalize Activations by Their RMS

RMS normalization controls activation scale while preserving a nonzero mean. For a row of identical positive values, the normalized result is close to one before applying weights.

The last-axis reduction treats each earlier index independently. A learned weight can change both magnitude and sign, so the weighted output need not have RMS one.

This NumPy adaptation keeps the upstream forward computation. It adds explicit input validation and independent examples; it does not implement PyTorch autograd.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/rmsnorm.py

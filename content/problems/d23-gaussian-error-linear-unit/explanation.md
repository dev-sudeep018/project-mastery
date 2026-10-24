# Explore a Smooth Gaussian Activation

The factor Phi(x) approaches zero for large negative inputs and one for large positive inputs. Around zero the curve smoothly connects these regimes; negative inputs need not map to zero.

GELU(x)-GELU(-x)=x follows from Gaussian symmetry. This relation is a useful check without duplicating the implementation.

Adapted the upstream exact erf equation to NumPy arrays with math.erf. The original gradient-flow task is outside this forward-only lesson.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/gelu.py

# Gate a Projection with SwiGLU

The gate can be negative because SiLU(g)=g\*sigmoid(g). Replacing it with sigmoid alone removes its amplitude and sign behavior.

A zero gate projection makes every output zero, while a nonzero value projection alone cannot restore the output. This exposes the multiplicative interaction.

Ported the upstream SwiGLU forward equation to NumPy and added stable sigmoid evaluation, explicit matrix conventions and immutable inputs.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/swiglu.py

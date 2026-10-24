# Rotate Query and Key Pairs with RoPE

Each pair undergoes a two-dimensional rotation, preserving its squared norm. Position zero is the identity transformation.

Applying the same positional shift to query and key changes each rotation but leaves their mutual dot product unchanged. The positional contribution depends on their relative separation, with content held fixed.

This adaptation ports the upstream paired rotation to NumPy and keeps its base of 10000. It omits gradient tracking and adds strict shapes and deterministic tests.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/rope.py

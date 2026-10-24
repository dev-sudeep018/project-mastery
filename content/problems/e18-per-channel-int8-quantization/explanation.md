# Quantize Linear Weights per Output Channel

The largest magnitude in each nonzero row maps to 127. Smaller weights share that row scale, so reconstruction introduces bounded rounding error.

The exercise uses a symmetric [-127,127] range and ties-to-even rounding. The upstream class clips to [-128,127] and adds a tiny denominator epsilon; this adaptation makes the zero-row behavior explicit instead.

Only weight storage is INT8 here. The forward pass reconstructs floating weights and performs a floating matmul. It is not an integer kernel or a demonstration of a fourfold total-model memory reduction.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/int8_quantization.py

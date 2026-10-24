# Track Retained Signal through Diffusion Steps

In the usual forward-noising parameterization, sqrt(alpha_bar) scales the original signal and sqrt(1-alpha_bar) scales independent unit-variance noise. These squared coefficients add to one.

Changing the number of steps while keeping beta endpoints fixed changes cumulative retention. The schedule itself is not a claim about image quality or a trained generation system.

Adapted only the upstream linear-beta branch, with configurable endpoints and both per-step betas and cumulative retention returned. Cosine and sigmoid variants are deliberately outside this contract.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/noise_schedule.py

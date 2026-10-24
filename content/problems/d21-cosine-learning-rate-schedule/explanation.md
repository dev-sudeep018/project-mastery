# Schedule Learning Rates with Warmup and Cosine Decay

Warmup controls the initial ramp independently of the decay floor. The minimum rate is the floor for the decay phase, not for warmup.

The peak occurs exactly at warmup_steps. At total_steps the cosine reaches its minimum, and clamping subsequent steps avoids an unintended second rise.

The schedule is adapted from the upstream scalar function. Added validation rules remove ambiguous configurations such as a warmup that occupies the entire schedule.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/cosine_lr.py

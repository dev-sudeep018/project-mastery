# Learn from Matched Pairs and In-Batch Negatives

Duplicated keys create indistinguishable candidates. Identical unit vectors on both sides can therefore still have loss log(N); alignment alone does not guarantee a near-zero loss.

Lower temperature sharpens the distribution. It helps when the positive score is largest and can amplify an incorrect match, so it does not universally reduce loss.

Adapted the upstream one-directional objective with explicit unit-vector checks, a documented temperature floor and shifted log probabilities. No encoder training is simulated.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/contrastive_loss.py

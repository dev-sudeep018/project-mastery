# Separate Batch Statistics from Running State

Training output centers each feature before applying gamma and beta. Running state accumulates information across batches; momentum here is the weight assigned to the newest batch.

Inference output for an example is independent of other rows in its batch when the saved state is fixed. This distinction matters when batch composition changes.

Adapted the upstream population-variance convention. Replaced in-place running-state updates with returned arrays and documented its difference from PyTorch’s running variance estimator.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/batchnorm.py

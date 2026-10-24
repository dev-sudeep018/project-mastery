# Keep Self and Neighbor Features Separate

Keeping self and neighbor features separate differs from adding a self loop to one shared average. The learned weight can emphasize either part independently.

Final normalization removes positive scale but preserves direction. A zero row stays zero, and rows with norms below 1e-8 use the denominator floor rather than being forced to unit length.

Adapted the upstream full-neighborhood GraphSAGE path. Removed optional random neighbor sampling and retained its ReLU and 1e-8 norm floor for deterministic browser practice.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/graphsage_layer.py

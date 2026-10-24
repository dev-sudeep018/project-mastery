# Normalize Messages in a Graph Convolution

The self connection lets a node retain its own features while receiving neighbor messages. Symmetric normalization moderates contributions from high-degree endpoints.

Relabeling nodes and applying the same permutation to adjacency rows, adjacency columns and feature rows must only relabel the output rows. Node numbering has no learned meaning here.

Ported the upstream symmetric GCN equation with explicit undirected-graph, zero-diagonal and shape contracts. Inputs remain unchanged; no graph library is required.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/gcn_layer.py

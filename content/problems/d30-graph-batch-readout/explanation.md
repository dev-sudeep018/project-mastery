# Pool Node Features into Graph Representations

Readout is invariant to node order within each graph. The three modes preserve different information: sums carry size, means average it away, and maxima emphasize the strongest value of each feature.

A maximum vector need not equal any particular node’s feature vector because different coordinates may come from different nodes.

Ported the upstream sum, mean and max readouts to NumPy. Added contiguous-ID validation so empty groups cannot silently create NaN or negative-infinity outputs.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/graph_readout.py

# Combine Causality with Padding

A causal mask stops a decoder position from reading future keys. A padding mask removes positions that do not represent real tokens in shorter sequences.

Combining the constraints also masks padded queries here. Such rows contain no allowed keys and must be handled deliberately by a downstream softmax implementation.

Inspect a sequence of length two in a padded length of four. Explain why masking only key columns leaves meaningless query rows, and why a mask convention must be documented before connecting APIs.

Concept reference: https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html

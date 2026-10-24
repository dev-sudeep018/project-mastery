# Turn Image Patches into a Token Sequence

Patch extraction changes layout; the learned projection then changes feature dimension. Keeping these operations conceptually separate makes ordering errors easier to spot.

A projection whose weight is an identity matrix exposes the extracted pixel order directly. This is useful when a plausible output shape hides a transposition error.

Adapted the upstream reshape/permute and affine projection to supplied NumPy weights. Rectangular images are supported; parameter initialization and autograd are omitted.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/vit_patch.py

# Add a Low-Rank Adapter to a Linear Layer

The adapter stores rank\*(input_features+output_features) parameters. It can be smaller than a full weight update when the chosen rank is sufficiently low; this is not a universal saving for every shape.

The two multiplications compute the same output as adding (alpha/rank)\*(b@a) to the base weight. A zero b initially leaves the base behavior unchanged.

The upstream class freezes its base layer and trains the adapter. This NumPy adaptation isolates the forward equation with supplied arrays; it does not simulate autograd or claim to verify training behavior.

Adapted code source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/lora.py

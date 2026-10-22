# Plan a Convolution’s Output Shape

Dilation spaces kernel taps apart, increasing the effective receptive field without increasing the number of weights. Padding adds available positions on both sides.

After subtracting effective kernel size from the padded input, integer division by stride counts complete shifts. Add one for the starting position.

Compare a three-tap kernel at dilation one and two. Explain why both have three weights while their required input span differs.

Concept reference: https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html

# Accumulate Gradients for Repeated Tokens

Lookup copies a shared parameter row into each token position. By the chain rule, all paths from that shared parameter to the loss contribute to its gradient.

Scatter-add reverses gather: each upstream row adds into its token’s row. Ordinary assignment loses earlier contributions for repeated tokens.

Give two occurrences equal and opposite gradients. Predict the shared row’s update, then explain why counting occurrences alone cannot determine a gradient.

Concept reference: https://numpy.org/doc/stable/reference/generated/numpy.ufunc.at.html

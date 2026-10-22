# Explain Inverted Dropout

A Bernoulli keep mask is one with probability 1-p. Dividing a kept activation by 1-p makes the expected training output equal to the input.

The supplied mask makes this lesson deterministic. A real dropout layer samples masks, but the scaling is based on the distribution's keep probability rather than the observed fraction kept in one batch.

Evaluation returns the input values because the training-time rescaling already accounts for missing activations. This is the inverted-dropout convention.

Compare a mask that keeps every entry with one that drops every entry. Neither outcome invalidates the expectation rule: it describes an average over random masks, not every individual pass. The expectation statement assumes masks are sampled with the stated probability.

## Further reading

- Dropout scaling convention: https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.dropout.Dropout.html

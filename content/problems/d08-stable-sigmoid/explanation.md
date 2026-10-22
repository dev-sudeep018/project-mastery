# Keep Sigmoid Stable at Extreme Inputs

Sigmoid maps a real-valued score into the interval from zero to one. Its slope is largest at zero and shrinks as the gate saturates.

For a positive input, exp(-x) is safe. For a negative input, exp(x)/(1+exp(x)) gives the same function without forming an enormous exponential.

Inspect the derivative at zero and at large magnitudes. Explain how saturated gates can weaken gradients even when the forward result is numerically valid.

Concept reference: https://d2l.ai/chapter_multilayer-perceptrons/mlp.html

# Correct Adam’s Early Moment Estimates

Adam tracks a moving average of gradients and of squared gradients. The second moment provides a separate adaptive scale for each coordinate.

Zero initialization shrinks early moment estimates. Bias correction divides by one minus the decay raised to the step count, while the stored state remains uncorrected.

For a constant gradient and zero initial moments, compare the corrected first and second moments over successive steps. Then explain why returning corrected moments as optimizer state would apply correction twice.

Concept reference: https://d2l.ai/chapter_optimization/adam.html

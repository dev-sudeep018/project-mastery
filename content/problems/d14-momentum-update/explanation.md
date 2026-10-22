# Carry Gradient History with Momentum

Momentum keeps a decayed sum of previous gradients. Consistent gradients reinforce one another, while alternating gradients can partially cancel.

Optimizer conventions differ. Here the current gradient enters unscaled, and the learning rate is applied only when updating parameters.

Set beta to zero to recover a plain gradient step. Then use a zero current gradient with nonzero velocity and explain why the parameters can still move.

Concept reference: https://d2l.ai/chapter_optimization/momentum.html

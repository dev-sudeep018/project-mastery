# Detect Conflicting Task Gradients

A negative dot product means a step improving one linearized task can worsen the other. Cosine similarity removes magnitude to isolate this directional disagreement.

The audit is local to the supplied gradients. It does not modify them or establish long-term task incompatibility, and zero gradients have no defined direction under the chosen zero convention.

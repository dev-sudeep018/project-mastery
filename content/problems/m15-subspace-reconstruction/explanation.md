# Measure What a Projection Loses

Projection takes dot products with basis directions. Orthonormal rows ensure each score measures a coordinate without counting the same direction twice.

Multiplying scores by the components returns to feature space; adding the supplied mean reverses centering. Missing directions cannot be recovered from the scores.

Compare a one-component reconstruction with a complete orthonormal basis. The full basis recovers every input; the smaller basis exposes the discarded residual.

Concept reference: https://scikit-learn.org/stable/modules/decomposition.html#pca

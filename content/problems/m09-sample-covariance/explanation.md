# Read Relationships with Covariance

Covariance describes joint variation around feature means. A positive off-diagonal entry means above-average values tend to occur together; a negative entry indicates opposing movement.

Rows are observations, so the centered transpose times the centered matrix has feature-by-feature shape. The n - 1 denominator is the requested sample estimator.

Add a different constant to every feature and compare the matrices. Then rescale one feature: covariance changes with units, which is why covariance and correlation answer different questions.

Concept reference: https://numpy.org/doc/stable/reference/generated/numpy.cov.html

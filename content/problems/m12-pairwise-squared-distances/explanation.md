# Compare Every Pair of Observations

Broadcasting a query axis against a candidate axis exposes all pairwise differences. Summing only the feature axis leaves the required query-by-candidate table.

Squared distance preserves nearest-neighbor ordering and avoids a square root. Its numeric values are not ordinary Euclidean distances, so a distance threshold must use matching units.

Translate both matrices by the same vector and compare results. Then translate only one. Use that experiment to explain why shared preprocessing matters.

Concept reference: https://numpy.org/doc/stable/user/basics.broadcasting.html

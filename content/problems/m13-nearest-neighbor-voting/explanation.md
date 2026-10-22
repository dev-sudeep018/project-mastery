# Make a Neighborhood Vote

Nearest-neighbor classification stores examples instead of fitting a coefficient vector. The metric and feature scale become part of the model.

Neighbor selection and class voting have separate ties. Stable distance ordering determines membership at the cutoff, then the smallest class wins a tied vote.

Change k for a query near a class boundary. Explain why increasing the neighborhood can reduce sensitivity to a single example while also hiding local structure.

Concept reference: https://scikit-learn.org/stable/modules/neighbors.html

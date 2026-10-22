# Assign Observations to Prototypes

The assignment step minimizes each observation’s squared distance while holding centers fixed. Center indices are cluster identities, not target classes.

Inertia sums squared distances, rather than averaging or taking square roots. Duplicating the dataset therefore doubles inertia without changing individual assignments.

Add a center exactly on a distant observation. Can inertia increase? Explain why a smaller training inertia alone does not tell you the best number of clusters.

Concept reference: https://scikit-learn.org/stable/modules/clustering.html#k-means

# Summarize Weighted Observations

Weights define how much each observation contributes to the summary. Normalizing by their sum makes a weight of two mean twice the influence, regardless of the overall scale.

Compute the mean first, then the weighted average of squared deviations. Centering before squaring also avoids subtracting two large nearly equal second moments.

Try multiplying every weight by ten. The summary must stay fixed. Then give an extreme observation zero weight and explain why it should have no effect.

Concept reference: https://numpy.org/doc/stable/reference/generated/numpy.average.html

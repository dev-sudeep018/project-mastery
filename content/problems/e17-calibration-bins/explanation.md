# Compare Forecasts with Observed Frequencies

A reliability table groups forecasts with similar predicted probabilities and compares their mean forecast with the observed fraction of positive outcomes.

The requested error weights each bin’s absolute gap by its share of observations. Empty bins carry no evidence and no weight; their zero values are placeholders.

Change the number of bins on a small sample. Explain why the estimate changes, why a low binned error is not proof of calibration, and why this diagnostic should accompany discrimination metrics.

Concept reference: https://scikit-learn.org/stable/modules/calibration.html

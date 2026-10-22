# Evaluate Probability Quality

The Brier score measures squared error of probability forecasts. A confident wrong forecast receives a larger penalty than an uncertain wrong forecast.

This binary convention uses a single probability for class one. It is not the sum of squared errors over two one-hot class columns, which would double the result.

Compare forecasts of 0.51 and 0.99 when the outcome is zero. Both cross a 0.5 decision threshold, but their losses differ. Explain what that adds beyond accuracy.

Concept reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html

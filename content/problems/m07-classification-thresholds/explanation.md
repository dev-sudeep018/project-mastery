# Investigate a Classification Threshold

The threshold is a decision rule layered on top of the score. With the same scores, reducing it cannot remove a predicted positive; both true-positive and false-positive counts can increase.

Precision divides true positives by all predicted positives. Recall divides true positives by all actual positives. F1 balances these ratios but does not encode the real cost of either mistake.

Choose and compare thresholds on validation data using the application's costs, then evaluate the chosen procedure on held-out data. This small example does not establish that a threshold is appropriate for a real deployment.

Try thresholds 0.3, 0.5, and 0.85 on the first example. Which errors change? Explain why a score of 0.8 is not automatically a trustworthy 80% probability without calibration evidence.

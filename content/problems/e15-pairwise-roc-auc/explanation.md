# Evaluate a Ranking without a Threshold

AUC measures ranking discrimination across thresholds. The pairwise view asks whether a randomly chosen positive example outranks a randomly chosen negative one.

Exact ties receive half credit, corresponding to no preference between the two examples. A one-class sample has no positive-negative pairs and cannot define this metric.

Apply a strictly increasing transformation to every score and compare AUC. Explain why the ranking stays fixed even though the values may no longer be calibrated probabilities.

Concept reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html

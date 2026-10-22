# Locate Classification Mistakes by Class

A confusion matrix preserves the direction of mistakes: true class a predicted as b is a different outcome from true b predicted as a.

Diagonal entries count correct decisions. Row sums show actual class support, while column sums show how often the model predicts each class.

Inspect a matrix where one rare class is always predicted as a common class. Explain how high overall accuracy can coexist with failure on that rare class.

Concept reference: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html

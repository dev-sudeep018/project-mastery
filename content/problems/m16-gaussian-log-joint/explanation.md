# Score a Gaussian Classifier in Log Space

Naive Bayes assumes features are conditionally independent given the class. That assumption turns a joint likelihood into a product of individual densities.

Logarithms turn the product into a sum. Adding log priors produces log-joint scores; normalizing them into probabilities is unnecessary for choosing the largest score.

Hold the feature parameters equal and change the priors. Then hold priors equal and change a variance. Explain why a broad Gaussian can be less confident near its mean but assign more density far away.

Concept reference: https://scikit-learn.org/stable/modules/naive_bayes.html#gaussian-naive-bayes

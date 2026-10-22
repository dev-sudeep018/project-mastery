# Measure Graded Retrieval Quality

DCG adds a relevance grade at each rank after discounting later positions. NDCG divides by an ideal score, making a perfect ordering score one when any positive judgment exists.

This lesson uses linear grades. Other implementations use exponential gains, so report the gain convention and cutoff with a metric rather than comparing differently defined numbers.

The ideal ranking includes relevant documents the system failed to retrieve. Restricting the denominator to the retrieved subset would reward omissions. This activity assigns zero to unjudged IDs; real evaluation must also examine judgment coverage.

Swap the two documents in the first example, then compare k=1 and k=2. Explain why recall at two can be unchanged while NDCG changes. A metric summarizes these judgments; it cannot prove that generated answers are factual.

## Further reading

- Linear-gain NDCG convention: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html

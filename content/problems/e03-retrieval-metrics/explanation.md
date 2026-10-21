# Recall@K and Mean Reciprocal Rank

Recall asks how much relevant material was recovered. MRR asks how far a reader must scan to find the first relevant result.

The metrics answer different questions. Retrieving one useful item first can yield perfect reciprocal rank while missing most relevant items.

Scores depend on the labels and query sample. A small teaching dataset supports debugging; it cannot establish production quality.

## Contract

- rankings and relevant are equal-length lists of lists of string IDs. k is a positive integer, excluding booleans.
- Deduplicate a ranking in order before taking k. Treat relevant IDs as a set.
- Recall is relevant retrieved / relevant available. Reciprocal rank is 1 / first relevant position, or zero.
- Queries with no relevant IDs contribute zero to both metrics. An empty query collection returns both zero. Raise ValueError for invalid inputs.

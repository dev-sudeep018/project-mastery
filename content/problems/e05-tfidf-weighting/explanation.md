# Build a TF-IDF Representation

Term frequency measures occurrences within a document; document frequency measures how widely a term is distributed across the corpus. Repeating a term in one document changes the former without changing the latter.

This activity fixes one explicit convention: natural term counts, smoothed inverse document frequency, then unit L2 row length. Other TF-IDF conventions exist, so compare formulas before comparing numbers.

Learn a vocabulary and idf on the reference corpus, then reuse them for queries. A zero query vector carries no lexical signal. Do not fit a new idf independently on each query.

Multiply every count in one document by the same positive integer. The normalized direction stays the same, while repeating just one term changes that direction. Connect these vectors to cosine retrieval and compare where lexical matching misses synonyms.

## Further reading

- TF-IDF convention: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html

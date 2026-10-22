# Build a Shared Document Vocabulary

A bag-of-words representation ignores token order but keeps occurrence counts. Its shared vocabulary maps each token to a consistent feature column.

Sorting the vocabulary makes the output deterministic. Counting unique tokens per document would instead produce binary presence features and lose repetition information.

Compare two documents with the same tokens in different orders. Then repeat one token. Explain which change this representation can detect and which it cannot.

Concept reference: https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction

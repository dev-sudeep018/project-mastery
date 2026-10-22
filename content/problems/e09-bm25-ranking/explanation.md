# Balance Term Frequency and Document Length

BM25 saturates term frequency: later repetitions contribute less than the first ones. Document-length normalization adjusts that contribution relative to the collection’s average length.

Document frequency counts rows containing a term, not total occurrences. This exercise uses Lucene’s positive IDF expression and explicitly includes the conventional k1 + 1 numerator factor.

Set b to zero and compare short and long documents with equal term counts. Then increase k1. Explain how these controls separately change length normalization and repetition saturation.

Concept reference: https://lucene.apache.org/core/9_12_1/core/org/apache/lucene/search/similarities/BM25Similarity.html

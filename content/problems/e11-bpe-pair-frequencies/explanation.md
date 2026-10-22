# Count Candidate Subword Merges

Byte-pair encoding repeatedly merges a frequent adjacent token pair. Pair statistics are weighted by word frequency so the model reflects the corpus, not merely a list of unique words.

Counting and merging have different overlap rules. The sequence a,a,a contains two adjacent a,a observations, even though a single left-to-right merge can consume only one of them.

Compare a common short word with a rare long word. Explain why unweighted pair counts can choose a different merge and produce a different vocabulary.

Concept reference: https://huggingface.co/learn/llm-course/chapter6/5

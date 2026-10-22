# Diversify a Retrieval Result

MMR makes selection depend on what is already in the result set. Once one passage is selected, a near duplicate receives a larger redundancy penalty.

This lesson supplies scores so you can inspect the selection rule without depending on an embedding model. Higher weight emphasizes query relevance; lower weight emphasizes diversity after the relevance-first seed.

This is a greedy procedure, not a guarantee of the globally best subset. Its outcome depends on score scaling and the candidate pool. Similarity alone also does not establish factual support for an answer.

For the first example, calculate both remaining candidates' scores by hand after choosing document zero. Then set weight to one and explain why the near duplicate returns. Compare the resulting context with rank fusion, which combines rankings but does not explicitly penalize redundancy.

## Further reading

- MMR: Goldstein and Carbonell (1998), https://aclanthology.org/X98-1025/

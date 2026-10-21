# Build the Retrieval Pipeline

The pipeline makes each boundary explicit: vectors become a ranking, rankings become a fused list, and relevance labels become metrics.

The provided keyword rankings isolate the fusion and evaluation logic from text tokenization. The project workbench exposes its simple keyword baseline so you can inspect that separate choice.

A passing pipeline confirms the contract on public examples. Your experiment report should still describe the teaching dataset's limits and identify a next evaluation that could challenge your conclusion.

## Contract

- Return a dictionary with rankings (one list of IDs per query), recall, and mrr.
- document_ids is a nonempty list of unique string IDs. document_vectors is (n,d), query_vectors is (q,d), with n,d,q positive and all values finite.
- lexical_rankings and relevant are lists of q lists containing only known IDs. Deduplicate each list; lexical rankings may omit documents.
- k is an integer 1..n, excluding booleans. vector_weight is a finite numeric scalar in [0,1], excluding booleans. Keyword weight is 1-vector_weight.
- Rank vector ties by document ID; fuse with the same tie rule. A zero vector has similarity zero. Queries with no relevant labels contribute zero metrics.
- Leave inputs unchanged and raise ValueError for invalid inputs. You may reuse your implementations of top_k_cosine, reciprocal_rank_fusion, and retrieval_metrics by including them in this file.

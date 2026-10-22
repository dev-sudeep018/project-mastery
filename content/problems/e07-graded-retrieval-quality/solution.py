import math
import numbers

def ndcg_at_k(ranked, relevance, k):
    if not isinstance(ranked, list) or not isinstance(relevance, dict) or type(k) is not int or k < 0:
        raise ValueError("Expected ID list, grade dictionary, and nonnegative integer cutoff")
    if any(not isinstance(x, str) or not x for x in [*ranked, *relevance]):
        raise ValueError("Document IDs must be nonempty strings")
    if any(not isinstance(v, numbers.Real) or isinstance(v, bool) or not math.isfinite(v) or not 0 <= v <= 5 for v in relevance.values()):
        raise ValueError("Relevance grades must be finite numbers in [0,5]")
    unique = list(dict.fromkeys(ranked))[:k]
    dcg = sum(float(relevance.get(doc, 0))/math.log2(rank+2) for rank,doc in enumerate(unique))
    ideal = sum(float(grade)/math.log2(rank+2) for rank,grade in enumerate(sorted(relevance.values(), reverse=True)[:k]))
    return dcg/ideal if ideal else 0.

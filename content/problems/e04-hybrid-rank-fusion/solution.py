import math
import numbers

def reciprocal_rank_fusion(rankings, rank_constant=60, weights=None, limit=None):
    if not isinstance(rankings,list) or not all(isinstance(row,list) and all(isinstance(x,str) for x in row) for row in rankings):
        raise ValueError("Expected lists of document IDs")
    if isinstance(rank_constant,bool) or not isinstance(rank_constant,numbers.Real) or not math.isfinite(rank_constant) or rank_constant <= 0:
        raise ValueError("Expected positive finite rank constant")
    if limit is not None and (type(limit) is not int or limit < 0):
        raise ValueError("Expected nonnegative integer limit")
    weights = [1.] * len(rankings) if weights is None else weights
    if not isinstance(weights,(list,tuple)) or len(weights) != len(rankings) or any(isinstance(w,bool) or not isinstance(w,numbers.Real) or not math.isfinite(w) or w < 0 for w in weights) or (weights and not any(w > 0 for w in weights)):
        raise ValueError("Expected matched nonnegative finite weights")
    scores = {}
    for ranking, weight in zip(rankings,weights):
        for rank, doc in enumerate(dict.fromkeys(ranking),1):
            scores[doc] = scores.get(doc,0.) + weight/(rank_constant+rank)
    return sorted(scores,key=lambda doc:(-scores[doc],doc))[:limit]

import numpy as np

def top_k_cosine(query, vectors, k):
    q, v = np.asarray(query,dtype=np.float64), np.asarray(vectors,dtype=np.float64)
    if q.ndim != 1 or q.size == 0 or v.ndim != 2 or v.shape[0] == 0 or v.shape[1] != q.size:
        raise ValueError("Incompatible nonempty vectors")
    if type(k) is not int or not 0 <= k <= v.shape[0] or not np.all(np.isfinite(q)) or not np.all(np.isfinite(v)):
        raise ValueError("Invalid k or non-finite vector")
    def normalize(a):
        scale = np.max(np.abs(a),axis=-1,keepdims=True)
        a = np.divide(a,scale,out=np.zeros_like(a),where=scale>0)
        length = np.linalg.norm(a,axis=-1,keepdims=True)
        return np.divide(a,length,out=np.zeros_like(a),where=length>0)
    scores = normalize(v) @ normalize(q)
    return np.lexsort((np.arange(len(v)),-scores))[:k].tolist()


def retrieval_metrics(rankings, relevant, k):
    def valid(groups):
        return isinstance(groups,list) and all(isinstance(row,list) and all(isinstance(x,str) for x in row) for row in groups)
    if not valid(rankings) or not valid(relevant) or len(rankings) != len(relevant) or type(k) is not int or k <= 0:
        raise ValueError("Expected matched string rankings and positive integer k")
    recall, mrr = 0., 0.
    for ranking, labels in zip(rankings,relevant):
        labels = set(labels)
        top = list(dict.fromkeys(ranking))[:k]
        if labels:
            recall += len(set(top) & labels) / len(labels)
            mrr += next((1/i for i,doc in enumerate(top,1) if doc in labels),0)
    n = len(rankings)
    return {"recall":recall/n if n else 0., "mrr":mrr/n if n else 0.}


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


def retrieval_pipeline(document_ids, document_vectors, query_vectors, lexical_rankings, relevant, k, vector_weight=0.5):
    if not isinstance(document_ids,list) or not document_ids or not all(isinstance(x,str) for x in document_ids) or len(set(document_ids)) != len(document_ids):
        raise ValueError("Expected unique document IDs")
    vectors, queries = np.asarray(document_vectors,dtype=np.float64), np.asarray(query_vectors,dtype=np.float64)
    if vectors.ndim != 2 or vectors.shape[0] != len(document_ids) or vectors.shape[1] == 0 or queries.ndim != 2 or queries.shape[0] == 0 or queries.shape[1] != vectors.shape[1]:
        raise ValueError("Incompatible vector shapes")
    if not np.all(np.isfinite(vectors)) or not np.all(np.isfinite(queries)):
        raise ValueError("Vectors must be finite")
    if type(k) is not int or not 1 <= k <= len(document_ids) or isinstance(vector_weight,bool) or not isinstance(vector_weight,numbers.Real) or not math.isfinite(vector_weight) or not 0 <= vector_weight <= 1:
        raise ValueError("Invalid k or vector weight")
    for groups in (lexical_rankings,relevant):
        if not isinstance(groups,list) or len(groups) != len(queries) or not all(isinstance(row,list) and all(isinstance(x,str) and x in document_ids for x in row) for row in groups):
            raise ValueError("Expected matched lists of known document IDs")
    # Pre-sort IDs so equal vector scores follow the project ID tie convention.
    order = sorted(range(len(document_ids)),key=lambda i:document_ids[i])
    ids = [document_ids[i] for i in order]
    vectors = vectors[order]
    rankings = []
    for query, lexical in zip(queries,lexical_rankings):
        vector = [ids[i] for i in top_k_cosine(query,vectors,len(ids))]
        rankings.append(reciprocal_rank_fusion([vector,lexical],weights=[vector_weight,1-vector_weight],limit=k))
    return {"rankings":rankings, **retrieval_metrics(rankings,relevant,k)}

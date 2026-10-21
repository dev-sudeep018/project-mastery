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

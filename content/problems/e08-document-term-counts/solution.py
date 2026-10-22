import numpy as np


def document_term_counts(documents):
    if not isinstance(documents,list) or not documents or any(not isinstance(doc,list) or any(not isinstance(t,str) or not t for t in doc) for doc in documents):
        raise ValueError("Expected tokenized documents")
    vocabulary = sorted({token for doc in documents for token in doc})
    columns = {token:i for i,token in enumerate(vocabulary)}
    counts = np.zeros((len(documents),len(vocabulary)), dtype=int)
    for row,doc in enumerate(documents):
        for token in doc:
            counts[row,columns[token]] += 1
    return {"vocabulary":vocabulary,"counts":counts}

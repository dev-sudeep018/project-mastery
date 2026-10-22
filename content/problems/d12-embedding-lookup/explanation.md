# Look Up Token Representations

An embedding table associates an integer vocabulary index with a dense feature vector. Lookup selects a row rather than performing arithmetic on the index.

Repeated tokens share parameters but occupy separate positions in the output sequence. Their outputs initially match because they read the same row.

Compare lookup with multiplying a one-hot matrix by the table. Explain why the direct indexing representation avoids allocating mostly zero entries.

Concept reference: https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html

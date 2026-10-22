import numpy as np


def merge_token_pair(tokens, pair):
    if not isinstance(tokens,list) or any(not isinstance(t,str) or not t for t in tokens) or not isinstance(pair,(list,tuple)) or len(pair) != 2 or any(not isinstance(t,str) or not t for t in pair):
        raise ValueError("Invalid tokens or merge pair")
    output, i = [], 0
    while i < len(tokens):
        if i+1 < len(tokens) and (tokens[i],tokens[i+1]) == tuple(pair):
            output.append(tokens[i]+tokens[i+1]); i += 2
        else:
            output.append(tokens[i]); i += 1
    return output

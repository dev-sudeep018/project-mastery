def chunk_text(text, chunk_size, overlap):
    if not isinstance(text,str) or type(chunk_size) is not int or type(overlap) is not int or chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Expected text, positive integer size, and valid integer overlap")
    words = text.split()
    result, start = [], 0
    while start < len(words):
        end = min(start+chunk_size,len(words))
        result.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += chunk_size-overlap
    return result

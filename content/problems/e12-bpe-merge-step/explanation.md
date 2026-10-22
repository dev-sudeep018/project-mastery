# Apply One Subword Merge

A BPE merge replaces a selected pair of adjacent tokens with one token. It operates on token boundaries rather than arbitrary substrings inside a token.

A left-to-right pass makes overlapping matches deterministic. Consuming a matched pair advances two positions, so neither original token is reused.

Compare the pair count for a,a,a with the number of replacements in one pass. Explain why pair statistics can count overlaps even though a concrete segmentation cannot contain overlapping tokens.

Concept reference: https://huggingface.co/learn/llm-course/chapter6/5

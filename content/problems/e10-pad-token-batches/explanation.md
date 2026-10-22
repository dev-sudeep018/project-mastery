# Distinguish Real Tokens from Padding

Padding makes sequence shapes compatible for batch operations. The presence mask records which entries have semantic content and which exist only to fill the rectangle.

Comparing token values with the padding identifier is insufficient when that identifier can also occur in real input. Length information preserves the distinction.

Use zero as both a real token and the padding value. Trace which positions a loss function should include and explain the error caused by masking every zero.

Concept reference: https://huggingface.co/docs/transformers/pad_truncation

# Vector Operations and Cosine Similarity

The dot product combines corresponding coordinates. Dividing by both vector lengths removes magnitude, leaving the cosine of the angle between them.

Scaling a vector by a positive number does not change its direction. Scaling by its largest absolute coordinate before computing a norm keeps arithmetic in a manageable range.

A zero vector has no angle. This exercise adopts an explicit 0.0 convention so later retrieval code can handle empty representations deterministically.

## Contract

- Accept numeric lists or NumPy arrays and leave both inputs unchanged.
- Return 0.0 if either vector is all zeros; zero has no direction.
- Raise ValueError for empty, mismatched, non-1D, or non-finite vectors.
- Handle large and tiny finite values without overflowing the norm.

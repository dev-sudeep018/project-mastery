# Deterministic Text Chunking

Overlap gives neighboring chunks shared context. Too much overlap increases duplication and indexing cost.

Determinism matters: the same text and settings should produce the same chunk boundaries every time.

Word chunking is a useful baseline. A production system may also need token budgets, sentence boundaries, metadata, and document-specific parsing.

## Contract

- chunk_size must be a positive integer; overlap must be an integer from 0 through chunk_size-1. Booleans are invalid.
- Advance by chunk_size - overlap words. Stop after emitting a window that reaches the final word.
- Return [] for empty or whitespace-only text. Do not emit a trailing window entirely contained in the previous window.
- Reject non-string text or invalid settings with ValueError. This exercise counts words, not model tokens.

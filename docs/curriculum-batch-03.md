# Thirty new learning activities

This batch expands the catalog from 21 to 51 lessons. The retrieval integration
checkpoint remains a separate package: 52 executable packages, 637 public cases,
three paths with 17 lessons each, four interactive experiments, and one project.
The new activities contribute 339 cases. None is counted merely for changing the
numbers in an existing exercise.

## Coverage and distinctions

| Path                        | New activities                                                                                                                                                                                                        | What learners investigate                                                                                                         |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Mathematics and ML, M08–M17 | Weighted moments, covariance, polynomial features, one-hot labels, pairwise distances, nearest-neighbor voting, cluster assignment, projection/reconstruction, Gaussian log-joint scores, stratified index allocation | Weight normalization, feature geometry, categorical representations, model decisions, information loss, and evaluation boundaries |
| Deep learning, D08–D17      | Stable sigmoid, cross-correlation, max pooling, convolution shapes, embedding lookup, embedding gradients, momentum, Adam, sinusoidal positions, causal/padding masks                                                 | Local operations, shared parameters, accumulated gradients, optimizer state, and sequence structure                               |
| AI engineering, E08–E17     | Document-term counts, BM25, token padding, BPE pair counts, BPE merge application, context selection, confusion matrices, ROC AUC, Brier score, calibration bins                                                      | Text representations, retrieval tradeoffs, token boundaries, resource budgets, discrimination, and probability quality            |

Each activity includes a contextual question, an explicit contract, three worked
examples, progressive hints, a reference, public edge-case checks, and a reflection
or small investigation. They extend the existing learning paths; there is no
competitive ranking or timed queue. Passing checks records practice, not mastery.

## Conventions that matter

- Weighted moments use population variance; covariance uses the sample denominator
  `n - 1`. Projection uses supplied orthonormal rows and a supplied training mean.
- Nearest-neighbor distance ties preserve training order; class-vote ties select
  the smallest class. Cluster ties select the lowest center index.
- Cross-correlation does not flip the kernel. Pooling drops incomplete trailing
  windows. Convolution geometry includes dilation and symmetric per-axis padding.
- Momentum uses an unscaled current gradient. Adam returns uncorrected stored
  moments, applies bias correction for the update, and places epsilon outside
  the square root.
- Attention masks are boolean with `True` meaning allowed. Padded query rows are
  completely masked. The downstream attention operation must handle such rows.
- BM25 uses Lucene's positive IDF expression, the conventional `k1 + 1` numerator,
  and an average document length that includes empty rows. This is an explicitly
  specified teaching implementation, not a claim of byte-for-byte Lucene scoring.
- BPE pair statistics count overlaps; applying one merge consumes original tokens
  without overlap. The context selector is a relevance-first greedy heuristic.
- ROC AUC gives half credit for exact score ties and requires both classes. Brier
  is the binary, single-probability mean squared error. Calibration uses equal-width
  bins, retains empty bins as zero placeholders, and weights gaps by occupancy.

## Source use

[Batch provenance](../content/batch-03-provenance.json) distinguishes references
from copied/adapted code for every new activity. The 21-source survey remains a
research inventory, not an import count.

D09 adapts the small `corr2d` loop from
[Dive into Deep Learning at the inspected revision](https://github.com/d2l-ai/d2l-en/blob/23d7a5aecceee57d1292c56e90cce307f183bb0a/chapter_convolutional-neural-networks/conv-layer.md).
Its upstream MIT-0 permission and copyright text are retained in the
[package notice](../content/problems/d09-image-cross-correlation/THIRD_PARTY_NOTICE.md)
and in the reference source delivered to the browser. Validation, examples,
tests, and lesson prose are original contributions. This does not relabel D2L's
entire book as Apache-licensed code.

The other 29 activities have original implementations and prose, with concept
references to NumPy, D2L, Hugging Face, PyTorch, scikit-learn, and Lucene. Source
references do not imply those projects endorsed or reviewed these activities.
No dataset, model weights, external API, or additional runtime library is needed.

## Verification approach

The fast batch check exercises references, incomplete starters, example counts,
and trivial wrong answers. Ten additional Python test methods check independent
properties, finite-difference embedding gradients, sigmoid overflow handling,
Adam trajectories, geometry, metric invariants, source notices, and 30 plausible
conceptual mistakes. Every misconception must fail a valid-input assertion,
rather than merely omit invalid-input validation.

The shared array assertion now distinguishes boolean masks from numeric zero/one
arrays. Public input-preservation cases use NumPy inputs where the contract allows
them. Embedding lookup also checks that changing its returned array cannot modify
the table. Browser tests discover all 52 references from the content directory.

Release results and remaining limitations are recorded in [verification.md](verification.md).
Further editorial review and learner feedback are still needed; automated checks
do not establish teaching effectiveness.

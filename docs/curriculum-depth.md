# Curriculum depth: the second batch

Nine original lessons extend the three paths to seven lessons each. The full
catalog now has 21 lessons plus the retrieval integration checkpoint, with 298
public cases. These are authored packages; the 2,000-item target remains a separate
editorial plan.

| Lesson                             | Learning objective                                                                       | Mode                                |
| ---------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------- |
| M05: training-only standardization | Find test-data leakage and reuse training statistics, including constant features        | Debug a supplied scaler             |
| M06: ridge gradients               | Separate an averaged data loss from an unaveraged weight penalty; leave bias unpenalized | Implement and investigate           |
| M07: classification thresholds     | Explain precision, recall, threshold ties, and empty-denominator conventions             | Implement and compare decisions     |
| D05: ReLU backward                 | Apply the activation gate to an upstream gradient without erasing its sign               | Trace the chain rule                |
| D06: inverted dropout              | Separate a supplied mask from keep probability and compare training/evaluation           | Investigate expected values         |
| D07: global gradient clipping      | Preserve direction using one norm across differently shaped parameter tensors            | Repair coordinate clipping          |
| E05: TF-IDF                        | Distinguish document frequency from term counts and normalize weighted rows              | Build a representation              |
| E06: MMR                           | Trade relevance against redundancy relative to all selected documents                    | Investigate a greedy selection rule |
| E07: NDCG                          | Evaluate graded relevance using actual rank order and a complete ideal ranking           | Compare evaluation conventions      |

Each lesson has a distinct contract, three worked examples, progressive hints,
interpretation prompts, a reference, and named public cases. The two debugging
starters are deliberately flawed and labelled as such. They are not reference
implementations.

## Conventions and sources

These are original teaching implementations, not wrappers around the referenced
libraries. They deliberately reject non-finite inputs and document their own
edge conventions. A matching formula does not imply complete API compatibility.

- M05 uses population variance and scale one for constant features, consistent
  with the documented [StandardScaler conventions](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).
- D06 uses training-time scaling by the keep probability, as described in
  [PyTorch Dropout](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.dropout.Dropout.html).
  The activity supplies a mask instead of sampling it; expectation claims assume
  masks sampled from the stated Bernoulli distribution.
- D07 treats the tensors as one concatenated gradient, following the norm
  interpretation in [clip*grad_norm*](https://docs.pytorch.org/docs/stable/generated/torch.nn.utils.clip_grad_norm_.html).
  This lesson returns copies and the original norm; it does not modify parameters.
- E05 fixes natural term counts, smoothed IDF, and L2 normalization, documented
  in [TfidfTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html).
- E06 teaches the relevance/redundancy rule from
  [Goldstein and Carbonell (1998)](https://aclanthology.org/X98-1025/).
  The lesson adds explicit relevance-first seeding, stable index ties, bounded
  supplied scores, and symmetric-similarity validation for reproducibility.
- E07 uses linear gains and logarithmic discount, matching the gain convention
  documented in [ndcg_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html).
  The lesson separately specifies duplicate IDs, unjudged documents, and cutoff
  behavior; it accepts an ordered ID list rather than predicted scores.

## Verification strategy

Public cases cover hand-calculated examples, shape/range validation, zero cases,
no input mutation, deterministic tie behavior, and copies where promised. Separate
Python tests check finite-difference gradients, train/test independence, exact
dropout expectation over all masks, clipping direction, normalized retrieval
vectors, and metric bounds. Every new evaluator also rejects a plausible
conceptual mistake on valid inputs. Native and browser execution are both part of
the release checks; CI checks do not substitute for independent educational review.

# Layer Normalization

Every row uses its own statistics. Unlike batch normalization, a row's result does not depend on which other examples share its batch.

Population variance divides by the feature count. The task is to normalize the observed features, not estimate a population from a statistical sample.

A constant row becomes zero before the affine transform, so its final value equals beta.

## Contract

- X is a nonempty 1D or 2D array; gamma and beta have shape (number_of_features,).
- Use population variance (ddof=0), not sample variance.
- Require finite inputs and a positive finite scalar eps; raise ValueError for invalid inputs.
- Return a NumPy array with the same shape as X. Do not modify inputs. Test values are moderate.

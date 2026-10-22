# Repair a Leaking Feature Scaler

A preprocessing step learns parameters too. Fitting it on test rows leaks information across the evaluation boundary, even if labels are never used.

The transform subtracts each training feature's mean and divides by its population standard deviation. Broadcasting applies the same learned arrays to every row.

Constant features receive a scale of one. If training always observes five but a test row contains nine, the transformed value is four, not zero.

After repairing the starter, add a distant test row and check that the training transform stays fixed. In a real pipeline, validation and test sets also reuse the training statistics; distribution shift should be observed, not silently normalized away.

## Further reading

- StandardScaler conventions: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html

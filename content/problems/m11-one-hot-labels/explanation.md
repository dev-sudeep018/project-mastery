# Represent Categories without an Ordering

One-hot encoding preserves category identity without assigning a distance along a single number line. Each observation selects exactly one coordinate.

The number of columns comes from the declared vocabulary, not the largest label in this batch. A missing class must not change the representation used by the model.

Try two batches that contain different subsets of labels. Explain why inferring the output width independently would break a shared classifier.

Concept reference: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html

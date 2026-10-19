# Numerically Stable Softmax

Softmax converts model scores, often called logits, into a probability distribution. It appears in classification and attention. A small numerical detail determines whether it works on real model outputs.

## Your task

Implement `softmax(x)` using NumPy. Accept a list or one-dimensional array of finite numbers, and return a NumPy array of the same shape. Probabilities must be nonnegative, finite, and sum to one within tolerance. Do not modify the input.

Raise `ValueError` for empty input, NaN, infinity, and arrays with more than one dimension. Inputs are numeric; conversion errors for nonnumeric values are outside this exercise.

## Example

`[1.0, 2.0, 3.0]` becomes approximately `[0.090031, 0.244728, 0.665241]`.

`[1000.0, 1001.0, 1002.0]` must produce the same probabilities. Taking the exponentials directly overflows.

## Why the shift works

Subtract the maximum score from every score before exponentiating. The largest exponential is now one; the others lie between zero and one. The common scaling factor cancels when dividing by the sum.

Underflow to zero for extremely unlikely outcomes is acceptable in finite precision. Dividing by a zero or infinite normalizer is not.

## Common mistakes

Direct exponentiation overflows for large scores. Normalizing the scores without exponentiation changes the function. In-place subtraction mutates the caller's input. Flattening input hides an invalid shape. Returning uniform probabilities passes an equal-scores example but fails unequal scores.

## Evaluation

Run examples checks three representative inputs. Check solution runs all public tests including invalid input, shift invariance, precision, and mutation. Absolute tolerance is 1e-7; relative tolerance is 1e-6. These are local practice checks, not hidden or independently verified assessments.

"""The same public evaluator runs in Python CI and in the browser."""
import numpy as np


def run_tests(namespace, mode="all"):
    fn = namespace.get("softmax")
    if not callable(fn):
        raise ValueError("Define a function named softmax(x).")
    results = []

    def check(name, values, expected=None, invalid=False):
        try:
            x = np.array(values, dtype=np.float64)
            original = x.copy()
            if invalid:
                try:
                    fn(x)
                except ValueError:
                    results.append(dict(name=name, passed=True, message="Correctly rejected invalid input."))
                    return
                raise AssertionError("Expected ValueError for this input.")
            actual = fn(x)
            assert isinstance(actual, np.ndarray), "Return a NumPy array."
            assert actual.shape == x.shape, f"Expected shape {x.shape}, received {actual.shape}."
            assert np.all(np.isfinite(actual)), "Output contains NaN or infinity. Shift scores before exp."
            assert np.all(actual >= 0), "Probabilities must be nonnegative."
            assert np.isclose(actual.sum(), 1, atol=1e-7, rtol=1e-6), "Probabilities must sum to 1."
            assert np.allclose(actual, expected, atol=1e-7, rtol=1e-6), f"Expected {np.array(expected)}, received {actual}."
            assert np.array_equal(x, original), "The input was modified. Avoid in-place operations."
            results.append(dict(name=name, passed=True, message="Output matches the expected probabilities."))
        except Exception as exc:
            results.append(dict(name=name, passed=False, message=f"{type(exc).__name__}: {exc}"[:600]))

    base = [0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
    check("Ordinary scores", [1, 2, 3], base)
    check("Large positive scores", [1000, 1001, 1002], base)
    check("Equal scores", [7, 7, 7, 7], [0.25] * 4)
    if mode == "sample":
        return results
    check("Large negative scores", [-1002, -1001, -1000], base)
    check("Single score", [42], [1])
    check("Dominant score", [-1000, 0, 1000], [0, 0, 1])
    check("Extreme finite scores", [-1e308, 1e308], [0, 1])
    check("Input remains unchanged", [3, 2, 1], base[::-1])
    check("Empty input", [], invalid=True)
    check("Invalid dimensions", [[1, 2], [3, 4]], invalid=True)
    check("Non-finite input", [1, float("nan")], invalid=True)
    check("Infinite input", [1, float("inf")], invalid=True)
    # Exercise the documented list input separately.
    try:
        actual = fn([1.0, 2.0, 3.0])
        assert isinstance(actual, np.ndarray) and actual.shape == (3,)
        assert np.allclose(actual, base, atol=1e-7, rtol=1e-6)
        results.append(dict(name="Python list input", passed=True, message="Accepts numeric lists."))
    except Exception as exc:
        results.append(dict(name="Python list input", passed=False, message=f"{type(exc).__name__}: {exc}"[:600]))
    return results

"""Small shared assertions, prepended to public evaluators at build time."""
import copy
import math
import numbers
import numpy as np


def assert_close(actual, expected, atol=1e-7, rtol=1e-6):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), "Return a dictionary with the documented keys."
        assert actual.keys() == expected.keys(), f"Expected keys {sorted(expected)}, got {sorted(actual)}."
        for key in expected:
            assert_close(actual[key], expected[key], atol, rtol)
    elif isinstance(expected, np.ndarray):
        assert isinstance(actual, np.ndarray), "Return a NumPy array."
        assert actual.shape == expected.shape, f"Expected shape {expected.shape}, got {actual.shape}."
        assert np.all(np.isfinite(actual)), "Result contains NaN or infinity."
        assert np.allclose(actual, expected, atol=atol, rtol=rtol), f"Expected {expected}, got {actual}."
    elif isinstance(expected, (list, tuple)):
        assert isinstance(actual, type(expected)), f"Return a {type(expected).__name__}."
        assert len(actual) == len(expected), f"Expected {len(expected)} items, got {len(actual)}."
        for left, right in zip(actual, expected):
            assert_close(left, right, atol, rtol)
    elif isinstance(expected, (bool, np.bool_)):
        assert isinstance(actual, (bool, np.bool_)) and actual == expected, "Return the expected boolean."
    elif isinstance(expected, numbers.Real):
        assert isinstance(actual, numbers.Real) and not isinstance(actual, (bool, np.bool_)), "Return a numeric scalar."
        assert math.isfinite(actual), "Result must be finite."
        assert math.isclose(actual, expected, abs_tol=atol, rel_tol=rtol), f"Expected {expected}, got {actual}."
    else:
        assert actual == expected, f"Expected {expected!r}, got {actual!r}."


def rejects(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except ValueError:
        return
    raise AssertionError("Raise ValueError for this invalid input.")


def unchanged(fn, *args, **kwargs):
    originals = copy.deepcopy((args, kwargs))
    result = fn(*args, **kwargs)
    assert_close(list(args), list(originals[0]))
    assert_close(kwargs, originals[1])
    return result


def run_cases(namespace, entrypoint, cases, mode="all"):
    fn = namespace.get(entrypoint)
    if not callable(fn):
        raise ValueError(f"Define the function {entrypoint} with the documented signature.")
    results = []
    for name, check in cases[:3] if mode == "sample" else cases:
        try:
            check(fn)
            results.append(dict(name=name, passed=True, message="Matches the documented behavior."))
        except Exception as exc:
            results.append(dict(name=name, passed=False, message=f"{type(exc).__name__}: {exc}"[:600]))
    return results

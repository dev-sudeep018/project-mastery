def run_tests(namespace, mode="all"):
    cases = [
        ("Same direction", lambda f: assert_close(f([1, 2], [2, 4]), 1.0)),
        ("Orthogonal vectors", lambda f: assert_close(f([1, 0], [0, 1]), 0.0)),
        ("Opposite direction", lambda f: assert_close(f([1, 0], [-3, 0]), -1.0)),
        ("Nontrivial angle", lambda f: assert_close(f([1, 1], [1, 0]), 2 ** -0.5)),
        ("Zero vector convention", lambda f: assert_close(f([0, 0], [1, 2]), 0.0)),
        ("Large finite vectors", lambda f: assert_close(f([1e308, 1e308], [1e308, 0]), 2 ** -0.5)),
        ("Tiny finite vectors", lambda f: assert_close(f([1e-300, 0], [1e-300, 0]), 1.0)),
        ("Inputs remain unchanged", lambda f: assert_close(unchanged(f, np.array([2., 1.]), np.array([2., 1.])), 1.0)),
        ("Mismatched lengths", lambda f: rejects(f, [1], [1, 2])),
        ("Empty vectors", lambda f: rejects(f, [], [])),
        ("Invalid dimensions", lambda f: rejects(f, [[1, 2]], [[1, 2]])),
        ("Non-finite input", lambda f: rejects(f, [float("inf")], [1])),
    ]
    return run_cases(namespace, 'cosine_similarity', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Repeated index accumulates', lambda f: assert_close(f([1,0,1], [[1,2],[3,4],[5,6]], 3), np.array([[3,4],[6,8],[0,0]]))),
        ('Contributions cancel', lambda f: assert_close(f([0,0], [[2,-3],[-2,3]], 1), np.zeros((1,2)))),
        ('Unused vocabulary rows', lambda f: assert_close(f([2], [[7]], 4), np.array([[0],[0],[7],[0]]))),
        ('Distinct tokens', lambda f: assert_close(f([1,0], [[2],[3]], 2), np.array([[3],[2]]))),
        ('Three repetitions', lambda f: assert_close(f([0,0,0], [[1],[2],[3]], 1), np.array([[6]]))),
        ('Reject missing upstream row', lambda f: rejects(f, [0,0], [[1]], 1)),
        ('Reject out-of-range token', lambda f: rejects(f, [1], [[1]], 1)),
        ('Reject fractional token', lambda f: rejects(f, [.5], [[1]], 2)),
        ('Reject empty tokens', lambda f: rejects(f, [], np.empty((0,1)), 2)),
        ('Reject non-finite gradient', lambda f: rejects(f, [0], [[np.nan]], 1)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([1, 0, 1]), np.array([[1, 2], [3, 4], [5, 6]]), 3), np.array([[3,4],[6,8],[0,0]]))),
    ]
    return run_cases(namespace, 'embedding_gradient', cases, mode)

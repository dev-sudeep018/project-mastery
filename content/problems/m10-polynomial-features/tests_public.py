def run_tests(namespace, mode="all"):
    cases = [
        ('Quadratic features', lambda f: assert_close(f([-2, 0, 3], 2), np.array([[1,-2,4],[1,0,0],[1,3,9]]))),
        ('Linear features', lambda f: assert_close(f([.5, -1], 1), np.array([[1,.5],[1,-1]]))),
        ('Cubic sign changes', lambda f: assert_close(f([-2], 3), np.array([[1,-2,4,-8]]))),
        ('Highest supported degree', lambda f: assert_close(f([1,-1], 5), np.array([[1,1,1,1,1,1],[1,-1,1,-1,1,-1]]))),
        ('Repeated inputs', lambda f: assert_close(f([2,2], 2), np.array([[1,2,4],[1,2,4]]))),
        ('Reject degree zero', lambda f: rejects(f, [1], 0)),
        ('Reject degree too large', lambda f: rejects(f, [1], 6)),
        ('Reject fractional degree', lambda f: rejects(f, [1], 2.5)),
        ('Reject boolean degree', lambda f: rejects(f, [1], True)),
        ('Reject empty vector', lambda f: rejects(f, [], 2)),
        ('Reject non-finite input', lambda f: rejects(f, [np.inf], 2)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([-2, 0, 3]), 2), np.array([[1,-2,4],[1,0,0],[1,3,9]]))),
    ]
    return run_cases(namespace, 'polynomial_features', cases, mode)

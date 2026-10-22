def run_tests(namespace, mode="all"):
    cases = [
        ('Horizontal edge response', lambda f: assert_close(f([[2,2,5,5]], [[1,-1]]), np.array([[0,-3,0]]))),
        ('Asymmetric filter', lambda f: assert_close(f([[1,2],[3,4]], [[1,2],[0,-1]]), np.array([[1]]))),
        ('One-pixel kernel', lambda f: assert_close(f([[1,-2],[3,0]], [[2]]), np.array([[2,-4],[6,0]]))),
        ('Overlapping windows', lambda f: assert_close(f([[1,2,3],[4,5,6]], [[1,1],[1,1]]), np.array([[12,16]]))),
        ('Vertical filter', lambda f: assert_close(f([[1],[3],[6]], [[-1],[1]]), np.array([[2],[3]]))),
        ('Zero filter', lambda f: assert_close(f([[1,2],[3,4]], [[0,0]]), np.zeros((2,1)))),
        ('Reject oversized filter', lambda f: rejects(f, [[1]], [[1,2]])),
        ('Reject empty filter', lambda f: rejects(f, [[1]], np.empty((0,1)))),
        ('Reject rank mismatch', lambda f: rejects(f, [1,2], [[1]])),
        ('Reject non-finite pixel', lambda f: rejects(f, [[np.nan]], [[1]])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[2, 2, 5, 5]]), np.array([[1, -1]])), np.array([[0,-3,0]]))),
    ]
    return run_cases(namespace, 'cross_correlate', cases, mode)

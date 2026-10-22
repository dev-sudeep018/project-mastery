def run_tests(namespace, mode="all"):
    cases = [
        ('Non-overlapping blocks', lambda f: assert_close(f([[1,4,2,3],[5,0,9,1]], (2,2), 2), np.array([[5,9]]))),
        ('Negative activations', lambda f: assert_close(f([[-4,-2],[-7,-3]], (2,2), 1), np.array([[-2]]))),
        ('Drop trailing partial window', lambda f: assert_close(f([[1,2,3,4,99]], (1,2), 2), np.array([[2,4]]))),
        ('Overlapping windows', lambda f: assert_close(f([[1,3,2,4]], (1,2), 1), np.array([[3,3,4]]))),
        ('Single-pixel pooling', lambda f: assert_close(f([[1,2],[3,4]], (1,1), 1), np.array([[1,2],[3,4]]))),
        ('Reject window too large', lambda f: rejects(f, [[1]], (2,1), 1)),
        ('Reject zero stride', lambda f: rejects(f, [[1]], (1,1), 0)),
        ('Reject fractional window', lambda f: rejects(f, [[1]], (1.5,1), 1)),
        ('Reject boolean stride', lambda f: rejects(f, [[1]], (1,1), True)),
        ('Reject non-finite input', lambda f: rejects(f, [[np.inf]], (1,1), 1)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[1, 4, 2, 3], [5, 0, 9, 1]]), (2, 2), 2), np.array([[5,9]]))),
    ]
    return run_cases(namespace, 'max_pool', cases, mode)

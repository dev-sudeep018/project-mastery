def run_tests(namespace, mode="all"):
    cases = [
        ('Directed mistakes', lambda f: assert_close(f([0,0,1,2], [1,1,1,0], 3), np.array([[0,2,0],[0,1,0],[1,0,0]]))),
        ('Absent classes retain axes', lambda f: assert_close(f([1,1], [1,1], 3), np.array([[0,0,0],[0,2,0],[0,0,0]]))),
        ('Perfect predictions', lambda f: assert_close(f([0,1,2], [0,1,2], 3), np.eye(3,dtype=int))),
        ('All predictions collapse', lambda f: assert_close(f([0,1,2], [0,0,0], 3), np.array([[1,0,0],[1,0,0],[1,0,0]]))),
        ('Single class', lambda f: assert_close(f([0,0], [0,0], 1), np.array([[2]]))),
        ('Reject out-of-range prediction', lambda f: rejects(f, [0], [2], 2)),
        ('Reject negative actual label', lambda f: rejects(f, [-1], [0], 2)),
        ('Reject different lengths', lambda f: rejects(f, [0,1], [0], 2)),
        ('Reject empty pairs', lambda f: rejects(f, [], [], 2)),
        ('Reject fractional prediction', lambda f: rejects(f, [0], [.5], 2)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([0, 0, 1, 2]), np.array([1, 1, 1, 0]), 3), np.array([[0,2,0],[0,1,0],[1,0,0]]))),
    ]
    return run_cases(namespace, 'confusion_matrix', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Repeated classes', lambda f: assert_close(f([2,0,2], 3), np.array([[0,0,1],[1,0,0],[0,0,1]]))),
        ('Missing batch classes', lambda f: assert_close(f([1], 4), np.array([[0,1,0,0]]))),
        ('Single-class vocabulary', lambda f: assert_close(f([0,0], 1), np.ones((2,1)))),
        ('Integer-valued floats', lambda f: assert_close(f([0.,1.], 2), np.eye(2))),
        ('Every class in reverse', lambda f: assert_close(f([2,1,0], 3), np.eye(3)[::-1])),
        ('Reject fractional label', lambda f: rejects(f, [1.5], 3)),
        ('Reject negative label', lambda f: rejects(f, [-1], 3)),
        ('Reject label at upper bound', lambda f: rejects(f, [3], 3)),
        ('Reject empty labels', lambda f: rejects(f, [], 2)),
        ('Reject boolean class count', lambda f: rejects(f, [0], True)),
        ('Reject non-finite label', lambda f: rejects(f, [np.nan], 2)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([2, 0, 2]), 3), np.array([[0,0,1],[1,0,0],[0,0,1]]))),
    ]
    return run_cases(namespace, 'one_hot', cases, mode)

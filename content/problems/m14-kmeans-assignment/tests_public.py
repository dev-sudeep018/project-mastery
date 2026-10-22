def run_tests(namespace, mode="all"):
    cases = [
        ('Two groups', lambda f: assert_close(f([[0],[2],[9]], [[0],[10]]), {'labels':np.array([0,0,1]), 'inertia':5.})),
        ('Tie chooses first center', lambda f: assert_close(f([[1]], [[0],[2]]), {'labels':np.array([0]), 'inertia':1.})),
        ('Squared rather than raw distance', lambda f: assert_close(f([[3,4]], [[0,0]]), {'labels':np.array([0]), 'inertia':25.})),
        ('Duplicate observations add cost', lambda f: assert_close(f([[2],[2]], [[0]]), {'labels':np.array([0,0]), 'inertia':8.})),
        ('Unused center is allowed', lambda f: assert_close(f([[0]], [[0],[20]]), {'labels':np.array([0]), 'inertia':0.})),
        ('Reject empty centers', lambda f: rejects(f, [[0]], np.empty((0,1)))),
        ('Reject empty observations', lambda f: rejects(f, np.empty((0,1)), [[0]])),
        ('Reject feature mismatch', lambda f: rejects(f, [[0,1]], [[0]])),
        ('Reject vector input', lambda f: rejects(f, [0], [[0]])),
        ('Reject non-finite center', lambda f: rejects(f, [[0]], [[np.nan]])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[0], [2], [9]]), np.array([[0], [10]])), {'labels':np.array([0,0,1]), 'inertia':5.})),
    ]
    return run_cases(namespace, 'assign_clusters', cases, mode)

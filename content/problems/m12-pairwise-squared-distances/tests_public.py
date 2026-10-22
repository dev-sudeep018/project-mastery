def run_tests(namespace, mode="all"):
    cases = [
        ('Rectangular comparison', lambda f: assert_close(f([[0,0],[3,4]], [[0,0],[1,0],[3,4]]), np.array([[0,1,25],[25,20,0]]))),
        ('Single feature', lambda f: assert_close(f([[-1],[2]], [[1]]), np.array([[4],[1]]))),
        ('Shared translation', lambda f: assert_close(f([[10,20]], [[13,24]]), np.array([[25]]))),
        ('Repeated candidates', lambda f: assert_close(f([[2,3]], [[2,3],[2,3]]), np.zeros((1,2)))),
        ('Negative features', lambda f: assert_close(f([[-2,-3]], [[1,1]]), np.array([[25]]))),
        ('Reject feature mismatch', lambda f: rejects(f, [[1,2]], [[1]])),
        ('Reject vector inputs', lambda f: rejects(f, [1,2], [1,2])),
        ('Reject empty rows', lambda f: rejects(f, np.empty((0,2)), [[1,2]])),
        ('Reject empty features', lambda f: rejects(f, np.empty((1,0)), np.empty((1,0)))),
        ('Reject non-finite value', lambda f: rejects(f, [[np.inf]], [[1]])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[0, 0], [3, 4]]), np.array([[0, 0], [1, 0], [3, 4]])), np.array([[0,1,25],[25,20,0]]))),
    ]
    return run_cases(namespace, 'pairwise_squared_distances', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Neighborhood majority', lambda f: assert_close(f([[0],[1],[2]], [0,1,1], [[.1]], 3), np.array([1]))),
        ('Stable distance tie', lambda f: assert_close(f([[-1],[1]], [9,2], [[0]], 1), np.array([9]))),
        ('Class vote tie', lambda f: assert_close(f([[0],[1]], [9,2], [[0]], 2), np.array([2]))),
        ('Several queries', lambda f: assert_close(f([[0,0],[3,4]], [2,7], [[0,1],[3,3]], 1), np.array([2,7]))),
        ('Sparse class identifiers', lambda f: assert_close(f([[1],[2],[3]], [100,100,4], [[3]], 3), np.array([100]))),
        ('Reject too many neighbors', lambda f: rejects(f, [[0]], [0], [[1]], 2)),
        ('Reject fractional class', lambda f: rejects(f, [[0]], [.2], [[1]], 1)),
        ('Reject mismatched labels', lambda f: rejects(f, [[0],[1]], [0], [[1]], 1)),
        ('Reject wrong query width', lambda f: rejects(f, [[0]], [0], [[1,2]], 1)),
        ('Reject zero k', lambda f: rejects(f, [[0]], [0], [[1]], 0)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[0], [1], [2]]), np.array([0, 1, 1]), np.array([[0.1]]), 3), np.array([1]))),
    ]
    return run_cases(namespace, 'knn_predict', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Saturating repetition without length penalty', lambda f: assert_close(f([[1],[3]], [1], 1, 0), np.array([np.log(1.2),1.5*np.log(1.2)]))),
        ('Term discrimination', lambda f: assert_close(f([[1,0],[0,1]], [1,0], 1, 1), np.array([np.log(2),0]))),
        ('Empty row in average length', lambda f: assert_close(f([[0],[2]], [1], 1, 1), np.array([0,np.log(2)]))),
        ('Repeated query term', lambda f: assert_close(f([[1,0],[0,1]], [2,0], 1, 0), np.array([2*np.log(2),0]))),
        ('Empty query', lambda f: assert_close(f([[2],[3]], [0], 1.2, .75), np.zeros(2))),
        ('All-empty corpus', lambda f: assert_close(f([[0,0],[0,0]], [1,1], 1, 1), np.zeros(2))),
        ('Reject fractional frequency', lambda f: rejects(f, [[.5]], [1], 1, 0)),
        ('Reject wrong query width', lambda f: rejects(f, [[1,2]], [1], 1, 0)),
        ('Reject zero k1', lambda f: rejects(f, [[1]], [1], 0, 0)),
        ('Reject b above one', lambda f: rejects(f, [[1]], [1], 1, 1.1)),
        ('Reject negative query count', lambda f: rejects(f, [[1]], [-1], 1, 0)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[1], [3]]), np.array([1]), 1, 0), np.array([np.log(1.2),1.5*np.log(1.2)]))),
    ]
    return run_cases(namespace, 'bm25_scores', cases, mode)

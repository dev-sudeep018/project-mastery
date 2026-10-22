def _independent_output(f):
    table = np.array([[1.,2.],[3.,4.]])
    output = f(table,[0,1])
    output[0,0] = 99
    assert_close(table,np.array([[1.,2.],[3.,4.]]))


def run_tests(namespace, mode="all"):
    cases = [
        ('Repeated tokens', lambda f: assert_close(f([[1,2],[3,4],[5,6]], [2,0,2]), np.array([[5,6],[1,2],[5,6]]))),
        ('One token', lambda f: assert_close(f([[-1,.5]], [0]), np.array([[-1,.5]]))),
        ('Order matters', lambda f: assert_close(f([[10],[20]], [1,0]), np.array([[20],[10]]))),
        ('Integer-valued IDs', lambda f: assert_close(f([[1],[2]], [0.,1.]), np.array([[1],[2]]))),
        ('Zero vectors are valid', lambda f: assert_close(f([[0,0],[1,1]], [0,0]), np.zeros((2,2)))),
        ('Reject out-of-range token', lambda f: rejects(f, [[1]], [1])),
        ('Reject negative token', lambda f: rejects(f, [[1]], [-1])),
        ('Reject fractional token', lambda f: rejects(f, [[1],[2]], [.5])),
        ('Reject empty token list', lambda f: rejects(f, [[1]], [])),
        ('Reject non-finite table', lambda f: rejects(f, [[np.inf]], [0])),
        ("Output does not alias the table", lambda f: _independent_output(f)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[1, 2], [3, 4], [5, 6]]), np.array([2, 0, 2])), np.array([[5,6],[1,2],[5,6]]))),
    ]
    return run_cases(namespace, 'embedding_lookup', cases, mode)

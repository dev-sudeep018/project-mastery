def run_tests(namespace, mode="all"):
    cases = [
        ('Different lengths', lambda f: assert_close(f([[2,3],[4]], 0), {'tokens':np.array([[2,3],[4,0]]),'mask':np.array([[True,True],[True,False]])})),
        ('Real token equals padding', lambda f: assert_close(f([[0],[]], 0), {'tokens':np.array([[0],[0]]),'mask':np.array([[True],[False]])})),
        ('All-empty batch', lambda f: assert_close(f([[],[]], 9), {'tokens':np.empty((2,0),dtype=int),'mask':np.empty((2,0),dtype=bool)})),
        ('Nonzero padding value', lambda f: assert_close(f([[],[1,2]], 7), {'tokens':np.array([[7,7],[1,2]]),'mask':np.array([[False,False],[True,True]])})),
        ('Equal lengths', lambda f: assert_close(f([[1],[2]], 0), {'tokens':np.array([[1],[2]]),'mask':np.ones((2,1),dtype=bool)})),
        ('Reject empty batch', lambda f: rejects(f, [], 0)),
        ('Reject negative token', lambda f: rejects(f, [[-1]], 0)),
        ('Reject fractional token', lambda f: rejects(f, [[1.5]], 0)),
        ('Reject negative pad ID', lambda f: rejects(f, [[1]], -1)),
        ('Reject boolean pad ID', lambda f: rejects(f, [[1]], True)),
        ("No input mutation", lambda f: assert_close(unchanged(f, [[2,3],[4]], 0), {'tokens':np.array([[2,3],[4,0]]),'mask':np.array([[True,True],[True,False]])})),
    ]
    return run_cases(namespace, 'pad_token_batch', cases, mode)

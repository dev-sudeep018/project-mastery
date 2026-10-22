def run_tests(namespace, mode="all"):
    cases = [
        ('Half kept', lambda f: assert_close(f([2,4], [True,False], .5, True), np.array([4.,0.]))),
        ('Evaluation bypasses mask', lambda f: assert_close(f([2,4], [False,False], .5, False), np.array([2.,4.]))),
        ('Drop probability convention', lambda f: assert_close(f([3,6], [True,True], .25, True), np.array([4.,8.]))),
        ('All dropped', lambda f: assert_close(f([1,2], [False,False], .5, True), np.zeros(2))),
        ('Zero probability applies supplied mask', lambda f: assert_close(f([1,2], [True,False], 0, True), np.array([1.,0.]))),
        ('Negative activations and matrix shape', lambda f: assert_close(f([[-2,3]], [[True,False]], .5, True), np.array([[-4.,0.]]))),
        ('No input mutation', lambda f: assert_close(unchanged(f, np.array([2.,4.]), np.array([True,False]), .5, True), np.array([4.,0.]))),
        ('Evaluation must copy', lambda f: assert_close(np.shares_memory((a := np.array([2.,4.])), f(a, [False,False], .5, False)), False)),
        ('Reject integer mask', lambda f: rejects(f, [1,2], [1,0], .5, True)),
        ('Reject broadcastable mask', lambda f: rejects(f, [[1,2]], [True,False], .5, True)),
        ('Reject drop probability one', lambda f: rejects(f, [1], [True], 1, True)),
        ('Reject negative probability', lambda f: rejects(f, [1], [True], -.1, True)),
        ('Reject vector probability', lambda f: rejects(f, [1], [True], [.5], True)),
        ('Reject nonboolean flag', lambda f: rejects(f, [1], [True], .5, 1)),
        ('Validate evaluation inputs too', lambda f: rejects(f, [np.nan], [True], .5, False)),
        ('Reject empty array', lambda f: rejects(f, [], np.array([], dtype=bool), .5, True)),
    ]
    return run_cases(namespace, 'inverted_dropout', cases, mode)

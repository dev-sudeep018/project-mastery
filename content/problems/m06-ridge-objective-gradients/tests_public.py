def run_tests(namespace, mode="all"):
    cases = [
        ('Fit is perfect, penalty remains', lambda f: assert_close(f([[1],[2]], [2,4], [2], 0, .5), {"loss":1.,"dw":np.array([1.]),"db":0.})),
        ('Bias is not penalized', lambda f: assert_close(f([[0]], [0], [0], 3, 10), {"loss":4.5,"dw":np.array([0.]),"db":3.})),
        ('Zero penalty', lambda f: assert_close(f([[1],[2]], [2,4], [0], 0, 0), {"loss":5.,"dw":np.array([-5.]),"db":-3.})),
        ('Two weights and signed penalty', lambda f: assert_close(f([[0,0],[0,0]], [0,0], [2,-3], 0, 2), {"loss":13.,"dw":np.array([4.,-6.]),"db":0.})),
        ('Penalty does not shrink with batch size', lambda f: assert_close(f([[0],[0],[0]], [0,0,0], [2], 0, 1)["dw"], np.array([2.]))),
        ('No input mutation', lambda f: assert_close(unchanged(f, np.array([[1.],[2.]]), np.array([2.,4.]), np.array([2.]), 0, .5)["loss"], 1.)),
        ('Reject negative strength', lambda f: rejects(f, [[1]], [0], [1], 0, -1)),
        ('Reject vector strength', lambda f: rejects(f, [[1]], [0], [1], 0, [1])),
        ('Reject nonfinite strength', lambda f: rejects(f, [[1]], [0], [1], 0, np.nan)),
        ('Reject vector bias', lambda f: rejects(f, [[1]], [0], [1], [0], 1)),
        ('Reject wrong target shape', lambda f: rejects(f, [[1]], [[0]], [1], 0, 1)),
        ('Reject wrong weight width', lambda f: rejects(f, [[1,2]], [0], [1], 0, 1)),
        ('Reject empty batch', lambda f: rejects(f, np.empty((0,1)), [], [1], 0, 1)),
        ('Reject nonfinite feature', lambda f: rejects(f, [[np.inf]], [0], [1], 0, 1)),
    ]
    return run_cases(namespace, 'ridge_gradients', cases, mode)

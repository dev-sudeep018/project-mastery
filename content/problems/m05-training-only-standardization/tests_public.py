def run_tests(namespace, mode="all"):
    cases = [
        ('Training statistics only', lambda f: assert_close(f([[1],[3]], [[5]]), {"mean":np.array([2.]), "scale":np.array([1.]), "train":np.array([[-1.],[1.]]), "test":np.array([[3.]])})),
        ('Constant training feature', lambda f: assert_close(f([[2,5],[4,5]], [[6,9]]), {"mean":np.array([3.,5.]), "scale":np.ones(2), "train":np.array([[-1.,0.],[1.,0.]]), "test":np.array([[3.,4.]])})),
        ('One training row', lambda f: assert_close(f([[4,8]], [[6,5]]), {"mean":np.array([4.,8.]), "scale":np.ones(2), "train":np.zeros((1,2)), "test":np.array([[2.,-3.]])})),
        ('Empty test matrix', lambda f: assert_close(f([[1],[3]], np.empty((0,1)))["test"], np.empty((0,1)))),
        ('Population variance', lambda f: assert_close(f([[0],[2],[4]], [[2]])["scale"], np.array([np.sqrt(8/3)]))),
        ('Test outlier cannot affect training', lambda f: assert_close(f([[1],[3]], [[1000000]])["train"], np.array([[-1.],[1.]]))),
        ('No input mutation', lambda f: assert_close(unchanged(f, np.array([[1.],[3.]]), np.array([[5.]]))["test"], np.array([[3.]]))),
        ('Reject empty training batch', lambda f: rejects(f, np.empty((0,2)), [[1,2]])),
        ('Reject empty training features', lambda f: rejects(f, np.empty((2,0)), np.empty((1,0)))),
        ('Reject wrong test width', lambda f: rejects(f, [[1,2]], [[3]])),
        ('Reject training vector', lambda f: rejects(f, [1,2], [[3]])),
        ('Reject test vector', lambda f: rejects(f, [[1],[2]], [3])),
        ('Reject nonfinite training', lambda f: rejects(f, [[np.nan]], [[1]])),
        ('Reject nonfinite test', lambda f: rejects(f, [[1]], [[np.inf]])),
    ]
    return run_cases(namespace, 'standardize_split', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ("Batch contributions", lambda f: assert_close(f([[1,2],[3,4]], [[1],[2]], [[1],[2]]), {"dx":np.array([[1,2],[2,4]]), "dw":np.array([[7],[10]]), "db":np.array([3])})),
        ("Multiple outputs", lambda f: assert_close(f([[1,2]], [[1,2],[3,4]], [[5,6]]), {"dx":np.array([[17,39]]), "dw":np.array([[5,6],[10,12]]), "db":np.array([5,6])})),
        ("Zero signal", lambda f: assert_close(f([[1]], [[2]], [[0]]), {"dx":np.array([[0]]), "dw":np.array([[0]]), "db":np.array([0])})),
        ("Negative signal", lambda f: assert_close(f([[2]], [[3]], [[-4]]), {"dx":np.array([[-12]]), "dw":np.array([[-8]]), "db":np.array([-4])})),
        ("Sum not average", lambda f: assert_close(f([[1],[1]], [[1]], [[1],[1]]), {"dx":np.array([[1],[1]]), "dw":np.array([[2]]), "db":np.array([2])})),
        ("Inputs unchanged", lambda f: assert_close(unchanged(f, np.array([[1.]]), np.array([[2.]]), np.array([[3.]])), {"dx":np.array([[6]]), "dw":np.array([[3]]), "db":np.array([3])})),
        ("Wrong weight shape", lambda f: rejects(f, [[1,2]], [[1]], [[1]])),
        ("Wrong gradient shape", lambda f: rejects(f, [[1]], [[1]], [[1,2]])),
        ("Empty batch", lambda f: rejects(f, np.empty((0,1)), [[1]], np.empty((0,1)))),
        ("Wrong rank", lambda f: rejects(f, [1], [[1]], [[1]])),
        ("Non-finite input", lambda f: rejects(f, [[float("nan")]], [[1]], [[1]])),
    ]
    return run_cases(namespace, 'linear_backward', cases, mode)

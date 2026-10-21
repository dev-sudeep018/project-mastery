def run_tests(namespace, mode="all"):
    cases = [
        ("One feature", lambda f: assert_close(f([[1],[2]], [2,4], [0], 0), {"loss": 5., "dw": np.array([-5.]), "db": -3.})),
        ("Perfect prediction", lambda f: assert_close(f([[1],[2]], [2,4], [2], 0), {"loss": 0., "dw": np.array([0.]), "db": 0.})),
        ("Two features", lambda f: assert_close(f([[1,0],[0,1]], [1,2], [0,0], 0), {"loss": 1.25, "dw": np.array([-.5,-1.]), "db": -1.5})),
        ("Bias contribution", lambda f: assert_close(f([[0],[0]], [1,3], [4], 1), {"loss": 1., "dw": np.array([0.]), "db": -1.})),
        ("Single example", lambda f: assert_close(f([[2,3]], [1], [1,1], 0), {"loss": 8., "dw": np.array([8.,12.]), "db": 4.})),
        ("Inputs remain unchanged", lambda f: assert_close(unchanged(f, np.array([[1.],[2.]]), np.array([2.,4.]), np.array([0.]), 0), {"loss": 5., "dw": np.array([-5.]), "db": -3.})),
        ("Empty batch", lambda f: rejects(f, np.empty((0,1)), [], [1], 0)),
        ("Wrong target length", lambda f: rejects(f, [[1],[2]], [1], [0], 0)),
        ("Wrong weight length", lambda f: rejects(f, [[1,2]], [1], [0], 0)),
        ("Non-finite feature", lambda f: rejects(f, [[float("nan")]], [1], [0], 0)),
        ("Non-scalar bias", lambda f: rejects(f, [[1]], [1], [0], [0])),
        ("Wrong target rank", lambda f: rejects(f, [[1]], [[1]], [0], 0)),
    ]
    return run_cases(namespace, 'linear_gradients', cases, mode)

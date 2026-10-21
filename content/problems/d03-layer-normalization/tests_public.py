def run_tests(namespace, mode="all"):
    cases = [
        ("Centered row", lambda f: assert_close(f([1,3],[1,1],[0,0]), np.array([-1,1])/np.sqrt(1+1e-5))),
        ("Constant row", lambda f: assert_close(f([5,5],[2,3],[1,2]), np.array([1.,2.]))),
        ("Independent rows", lambda f: assert_close(f([[1,3],[11,13]],[1,1],[0,0]), np.array([[-1,1],[-1,1]])/np.sqrt(1+1e-5))),
        ("Scale and shift", lambda f: assert_close(f([1,3],[2,3],[4,5],3), np.array([3.,6.5]))),
        ("Single feature", lambda f: assert_close(f([[4],[9]],[2],[3]), np.array([[3.],[3.]]))),
        ("Population variance", lambda f: assert_close(f([0,2],[1,1],[0,0],1), np.array([-1,1])/np.sqrt(2))),
        ("Inputs unchanged", lambda f: assert_close(unchanged(f, np.array([2.,2.]), np.array([1.,1.]), np.array([0.,0.])), np.array([0.,0.]))),
        ("Empty features", lambda f: rejects(f, [], [], [])),
        ("Wrong gamma shape", lambda f: rejects(f, [1,2], [1], [0,0])),
        ("Wrong rank", lambda f: rejects(f, [[[1]]], [1], [0])),
        ("Non-finite value", lambda f: rejects(f, [float("inf")], [1], [0])),
        ("Invalid epsilon", lambda f: rejects(f, [1], [1], [0], 0)),
    ]
    return run_cases(namespace, 'layer_norm', cases, mode)

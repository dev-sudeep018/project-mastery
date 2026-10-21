def run_tests(namespace, mode="all"):
    cases = [
        ("Uniform weights", lambda f: assert_close(f([[0]],[[1],[2]],[[2],[6]],[[True,True]]), {"weights":np.array([[.5,.5]]),"output":np.array([[4.]])})),
        ("One permitted key", lambda f: assert_close(f([[1]],[[1],[2]],[[2],[6]],[[True,False]]), {"weights":np.array([[1.,0.]]),"output":np.array([[2.]])})),
        ("Entirely masked row", lambda f: assert_close(f([[1]],[[1]],[[7]],[[False]]), {"weights":np.array([[0.]]),"output":np.array([[0.]])})),
        ("Weighted values", lambda f: assert_close(f([[1]],[[0],[math.log(3)]],[[0],[4]],[[True,True]]), {"weights":np.array([[.25,.75]]),"output":np.array([[3.]])})),
        ("Dimension scaling", lambda f: assert_close(f([[1,0]],[[0,0],[math.log(3)*math.sqrt(2),0]],[[0],[4]],[[True,True]]), {"weights":np.array([[.25,.75]]),"output":np.array([[3.]])})),
        ("Large scores", lambda f: assert_close(f([[1000]],[[1000],[1000]],[[2],[4]],[[True,True]]), {"weights":np.array([[.5,.5]]),"output":np.array([[3.]])})),
        ("Inputs unchanged", lambda f: assert_close(unchanged(f, np.array([[0.]]),np.array([[1.]]),np.array([[2.]]),np.array([[True]])), {"weights":np.array([[1.]]),"output":np.array([[2.]])})),
        ("Numeric mask rejected", lambda f: rejects(f, [[1]],[[1]],[[1]],[[1]])),
        ("Mask shape rejected", lambda f: rejects(f, [[1]],[[1]],[[1]],[True])),
        ("Key dimension rejected", lambda f: rejects(f, [[1,2]],[[1]],[[1]],[[True]])),
        ("Value length rejected", lambda f: rejects(f, [[1]],[[1]],[[1],[2]],[[True]])),
        ("Non-finite query", lambda f: rejects(f, [[float("nan")]],[[1]],[[1]],[[True]])),
    ]
    return run_cases(namespace, 'masked_attention', cases, mode)

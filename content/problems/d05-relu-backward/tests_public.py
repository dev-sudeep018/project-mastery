def run_tests(namespace, mode="all"):
    cases = [
        ('Gate follows activation', lambda f: assert_close(f([-2,0,3], [5,7,-4]), {"output":np.array([0.,0.,3.]),"dx":np.array([0.,0.,-4.])})),
        ('Matrix activations', lambda f: assert_close(f([[-1,2],[3,-4]], [[1,2],[3,4]]), {"output":np.array([[0.,2.],[3.,0.]]),"dx":np.array([[0.,2.],[3.,0.]])})),
        ('Zero boundary', lambda f: assert_close(f([0,0], [1,-1]), {"output":np.zeros(2),"dx":np.zeros(2)})),
        ('Negative upstream survives', lambda f: assert_close(f([1,2], [-3,-4])["dx"], np.array([-3.,-4.]))),
        ('All negative activations', lambda f: assert_close(f([-1,-2], [3,4])["dx"], np.zeros(2))),
        ('Three dimensional shape', lambda f: assert_close(f(np.ones((2,1,3)), -np.ones((2,1,3)))["dx"], -np.ones((2,1,3)))),
        ('No input mutation', lambda f: assert_close(unchanged(f, np.array([-1.,2.]), np.array([3.,-4.]))["dx"], np.array([0.,-4.]))),
        ('Reject broadcastable gradient', lambda f: rejects(f, [[1,2],[3,4]], [1,2])),
        ('Reject scalar activation', lambda f: rejects(f, 1, 2)),
        ('Reject empty array', lambda f: rejects(f, [], [])),
        ('Reject nonfinite activation', lambda f: rejects(f, [np.inf], [1])),
        ('Reject nonfinite gradient', lambda f: rejects(f, [1], [np.nan])),
    ]
    return run_cases(namespace, 'relu_backward', cases, mode)

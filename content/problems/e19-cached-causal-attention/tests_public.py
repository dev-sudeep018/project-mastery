def run_tests(namespace, mode="all"):
    cases = [
        ('First token', lambda f: assert_close(f([[1]],[[1]],[[7]]),{"output":np.array([[7.]]),"keys":np.array([[1.]]),"values":np.array([[7.]])})),
        ('Two-token prefill', lambda f: assert_close(f([[0],[0]],[[0],[0]],[[2],[4]]),{"output":np.array([[2.],[3.]]),"keys":np.zeros((2,1)),"values":np.array([[2.],[4.]])})),
        ('Continue a cached prefix', lambda f: assert_close(f([[0],[0]],[[0],[0]],[[20],[30]],([[0]],[[10]])),{"output":np.array([[15.],[20.]]),"keys":np.zeros((3,1)),"values":np.array([[10.],[20.],[30.]])})),
        ('Scale by key dimension', lambda f: assert_close(f([[1,1]],[[0,0]],[[0]],([[1,1]],[[1]]))["output"],np.array([[1/(1+np.exp(-np.sqrt(2)))] ]))),
        ('Large scores stay finite', lambda f: assert_close(f([[1000]],[[1000]],[[9]],([[-1000]],[[2]]))["output"],np.array([[9.]]))),
        ('Empty cache allowed', lambda f: assert_close(f([[0]],[[0]],[[4]],(np.empty((0,1)),np.empty((0,1))))["output"],np.array([[4.]]))),
        ('Value width differs from key width', lambda f: assert_close(f([[0]],[[0]],[[2,4]])["output"],np.array([[2.,4.]]))),
        ('Reject cache container', lambda f: rejects(f,[[0]],[[0]],[[1]],[])),
        ('Reject cache length mismatch', lambda f: rejects(f,[[0]],[[0]],[[1]],([[1]],[[1],[2]]))),
        ('Reject query shape', lambda f: rejects(f,[[0,0]],[[0]],[[1]])),
        ('Reject nonfinite cache', lambda f: rejects(f,[[0]],[[0]],[[1]],([[np.nan]],[[1]]))),
        ('No mutation', lambda f: assert_close(unchanged(f,np.zeros((1,1)),np.zeros((1,1)),np.array([[20.]]),(np.zeros((1,1)),np.array([[10.]])))["output"],np.array([[15.]])))
    ]
    return run_cases(namespace, 'cached_attention', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Isolated node', lambda f: assert_close(f([[0]],[[3,4]],[[1,0],[0,1],[0,0],[0,0]]),np.array([[.6,.8]]))),
        ('Self and neighbor directions', lambda f: assert_close(f([[0,1],[1,0]],[[2],[4]],np.eye(2)),np.array([[2,4],[4,2]])/np.sqrt(20))),
        ('Zero output', lambda f: assert_close(f([[0]],[[0]],[[1],[1]]),np.array([[0.]]))),
        ('Mean rather than sum', lambda f: assert_close(f([[0,1,1],[0,0,0],[0,0,0]],[[1],[2],[4]],np.eye(2))[0],np.array([1,3])/np.sqrt(10))),
        ('Ignore edge strength', lambda f: assert_close(f([[0,10],[1,0]],[[2],[4]],np.eye(2)),np.array([[2,4],[4,2]])/np.sqrt(20))),
        ('ReLU before normalization', lambda f: assert_close(f([[0]],[[-1]],[[1],[0]]),np.zeros((1,1)))),
        ('Norm floor', lambda f: assert_close(f([[0]],[[1e-10]],[[1],[0]]),np.array([[.01]]))),
        ('Reject wrong weight rows', lambda f: rejects(f,[[0]],[[1]],[[1]])),
        ('Reject self edge', lambda f: rejects(f,[[1]],[[1]],[[1],[1]])),
        ('Reject negative edge', lambda f: rejects(f,[[0,-1],[0,0]],[[1],[1]],[[1],[1]])),
        ('Reject nonfinite input', lambda f: rejects(f,[[0]],[[np.inf]],[[1],[1]])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([[0.]]),np.array([[3.,4.]]),np.array([[1.,0.],[0.,1.],[0.,0.],[0.,0.]])),np.array([[.6,.8]])))
    ]
    return run_cases(namespace, 'graphsage_layer', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Isolated node', lambda f: assert_close(f([[0]],[[2,-1]],[[1],[1]]),np.array([[1.]]))),
        ('Connected pair', lambda f: assert_close(f([[0,1],[1,0]],[[2],[4]],[[1]]),np.array([[3.],[3.]]))),
        ('Apply ReLU after aggregation', lambda f: assert_close(f([[0]],[[-2]],[[1]]),np.array([[0.]]))),
        ('Unequal degrees', lambda f: assert_close(f([[0,1,0],[1,0,1],[0,1,0]],[[1],[0],[0]],[[1]]),np.array([[.5],[1/np.sqrt(6)],[0.]]))),
        ('Weighted edge', lambda f: assert_close(f([[0,2],[2,0]],[[1],[4]],[[1]]),np.array([[3.],[2.]]))),
        ('No edges', lambda f: assert_close(f(np.zeros((2,2)),[[2,-1],[1,3]],np.eye(2)),np.array([[2,0],[1,3]]))),
        ('Reject directed graph', lambda f: rejects(f,[[0,1],[0,0]],[[1],[1]],[[1]])),
        ('Reject existing self edges', lambda f: rejects(f,[[1]],[[1]],[[1]])),
        ('Reject negative edge', lambda f: rejects(f,[[0,-1],[-1,0]],[[1],[1]],[[1]])),
        ('Reject feature mismatch', lambda f: rejects(f,[[0]],[[1,2]],[[1]])),
        ('Reject empty graph', lambda f: rejects(f,np.empty((0,0)),np.empty((0,1)),[[1]])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([[0.,1.],[1.,0.]]),np.array([[2.],[4.]]),np.ones((1,1))),np.array([[3.],[3.]])))
    ]
    return run_cases(namespace, 'gcn_layer', cases, mode)

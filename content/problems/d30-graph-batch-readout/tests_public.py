def run_tests(namespace, mode="all"):
    cases = [
        ('Mean with interleaved nodes', lambda f: assert_close(f([[1,2],[9,8],[3,4]],[0,1,0]),np.array([[2,3],[9,8]]))),
        ('Sum per graph', lambda f: assert_close(f([[1,2],[9,8],[3,4]],[0,1,0],"sum"),np.array([[4,6],[9,8]]))),
        ('Negative maxima', lambda f: assert_close(f([[-2,-5],[-3,-1]],[0,0],"max"),np.array([[-2,-1]]))),
        ('Unequal graph sizes', lambda f: assert_close(f([[2],[4],[6],[9]],[0,0,0,1]),np.array([[4.],[9.]]))),
        ('One node per graph', lambda f: assert_close(f([[3],[2]],[1,0]),np.array([[2.],[3.]]))),
        ('Coordinate-wise max', lambda f: assert_close(f([[3,1],[1,4]],[0,0],"max"),np.array([[3,4]]))),
        ('Reject missing graph ID', lambda f: rejects(f,[[1],[2]],[0,2])),
        ('Reject invalid ID types', lambda f: [rejects(f,[[1]],ids) for ids in ([0.0],[False],[-1])]),
        ('Reject unsupported mode', lambda f: rejects(f,[[1]],[0],"median")),
        ('Reject batch length', lambda f: rejects(f,[[1],[2]],[0])),
        ('Reject empty graph batch', lambda f: rejects(f,np.empty((0,2)),np.array([],dtype=int))),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([[1.],[3.]]),np.array([0,0])),np.array([[2.]])))
    ]
    return run_cases(namespace, 'graph_readout', cases, mode)

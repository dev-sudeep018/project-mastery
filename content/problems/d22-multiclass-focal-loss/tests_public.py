def run_tests(namespace, mode="all"):
    cases = [
        ('Uniform binary prediction', lambda f: assert_close(f([[0,0]],[0],1,0),np.log(2))),
        ('Focus uniform prediction', lambda f: assert_close(f([[0,0]],[0],1,2),np.log(2)/4)),
        ('Confident wrong prediction', lambda f: assert_close(f([[1000,-1000]],[1]),500)),
        ('Batch mean', lambda f: assert_close(f([[0,0],[1000,-1000]],[0,0],1,0),np.log(2)/2)),
        ('Single class', lambda f: assert_close(f([[4],[2]],[0,0]),0)),
        ('Zero alpha', lambda f: assert_close(f([[1,2]],[0],0,2),0)),
        ('Reject floating labels', lambda f: rejects(f,[[1,2]],[0.0])),
        ('Reject boolean labels', lambda f: rejects(f,[[1,2]],[True])),
        ('Reject unknown label', lambda f: rejects(f,[[1,2]],[2])),
        ('Reject invalid gamma', lambda f: [rejects(f,[[1,2]],[0],1,value) for value in (-1,2**4096)]),
        ('Reject empty batch', lambda f: rejects(f,np.empty((0,2)),np.array([],dtype=int))),
        ('No mutation', lambda f: assert_close(unchanged(f,np.zeros((1,2)),np.array([0]),1,0),np.log(2)))
    ]
    return run_cases(namespace, 'focal_loss', cases, mode)

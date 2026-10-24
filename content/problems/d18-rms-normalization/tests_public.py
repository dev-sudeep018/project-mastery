def run_tests(namespace, mode="all"):
    cases = [
        ('Constant activations', lambda f: assert_close(f([2,2],[1,1],1), np.array([2/np.sqrt(5)]*2))),
        ('Feature scaling', lambda f: assert_close(f([3,4],[2,-1],.5), np.array([6,-4])/np.sqrt(13))),
        ('Zero activations', lambda f: assert_close(f([[0,0]],[3,4]), np.zeros((1,2)))),
        ('Independent rows', lambda f: assert_close(f([[1,1],[2,2]],[1,2],1), np.array([[1,2]]) * np.array([[1/np.sqrt(2)],[2/np.sqrt(5)]]))),
        ('Three dimensions', lambda f: assert_close(f(np.ones((2,3,4)),np.ones(4),3),np.full((2,3,4),.5))),
        ('Negative activations', lambda f: assert_close(f([-2,-2],[1,1],1),np.array([-2,-2])/np.sqrt(5))),
        ('Reject mismatched weights', lambda f: rejects(f,[[1,2]],[1])),
        ('Reject empty axis', lambda f: rejects(f,np.empty((2,0)),[])),
        ('Reject zero epsilon', lambda f: rejects(f,[1],[1],0)),
        ('Reject invalid epsilon', lambda f: [rejects(f,[1],[1],value) for value in (True,2**4096)]),
        ('Reject nonfinite input', lambda f: rejects(f,[np.inf],[1])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([2.,2.]),np.ones(2),1),np.array([2,2])/np.sqrt(5)))
    ]
    return run_cases(namespace, 'rms_norm', cases, mode)

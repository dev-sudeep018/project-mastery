def run_tests(namespace, mode="all"):
    cases = [
        ('Base plus update', lambda f: assert_close(f([[1,2]],[[3,4]],[1],[[1,0]],[[2]]),np.array([[14]]))),
        ('Disabled adapter', lambda f: assert_close(f([[1,2]],[[3,4]],[1],[[1,0]],[[2]],0),np.array([[12]]))),
        ('Rank scaling', lambda f: assert_close(f([2],[[0]],[1],[[1],[2]],[[3,4]],2),np.array([23]))),
        ('Zero B preserves base', lambda f: assert_close(f([[1,2]],[[3,4]],[1],[[1,0]],[[0]]),np.array([[12]]))),
        ('Leading batch dimensions', lambda f: assert_close(f(np.ones((2,3,2)),np.eye(2),[1,2],[[1,0]],[[1],[2]]),np.tile([3,5],(2,3,1)))),
        ('Negative adapter entries', lambda f: assert_close(f([2],[[3]],[-1],[[-2]],[[4]],.5),np.array([-3]))),
        ('Reject incompatible rank', lambda f: rejects(f,[1],[[1]],[0],[[1]],[[1,2]])),
        ('Reject bias broadcast', lambda f: rejects(f,[1],[[1]],[0,0],[[1]],[[1]])),
        ('Reject empty rank', lambda f: rejects(f,[1],[[1]],[0],np.empty((0,1)),np.empty((1,0)))),
        ('Reject invalid alpha', lambda f: [rejects(f,[1],[[1]],[0],[[1]],[[1]],value) for value in (-1,2**4096)]),
        ('Reject nonfinite weight', lambda f: rejects(f,[1],[[np.inf]],[0],[[1]],[[1]])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([[1.,2.]]),np.array([[3.,4.]]),np.array([1.]),np.array([[1.,0.]]),np.array([[2.]])),np.array([[14]])))
    ]
    return run_cases(namespace, 'lora_linear', cases, mode)

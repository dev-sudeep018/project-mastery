def run_tests(namespace, mode="all"):
    cases = [
        ('Exactly represented row', lambda f: assert_close(f([[1,2]],[[127,-127]],[3]),dict(weight_int8=np.array([[127,-127]],dtype=np.int8),scale=np.array([[1.]]),output=np.array([[-124.]])))),
        ('Independent scales', lambda f: assert_close(f([2],[[127],[254]],[0,1]),dict(weight_int8=np.array([[127],[127]],dtype=np.int8),scale=np.array([[1.],[2.]]),output=np.array([254.,509.])))),
        ('Zero row', lambda f: assert_close(f([4,5],[[0,0]],[7]),dict(weight_int8=np.zeros((1,2),dtype=np.int8),scale=np.array([[1.]]),output=np.array([7.])))),
        ('Ties to even', lambda f: assert_close(f([1,1,1,1],[[127,.5,1.5,-1.5]],[0])["weight_int8"],np.array([[127,0,2,-2]],dtype=np.int8))),
        ('Actual int8 storage', lambda f: assert_close(f([1],[[1]],[0])["weight_int8"].dtype == np.dtype(np.int8), True)),
        ('Batched inference', lambda f: assert_close(f(np.ones((2,3,1)),[[127]],[1])["output"],np.full((2,3,1),128.))),
        ('Reject rank mismatch', lambda f: rejects(f,[1],[1],[0])),
        ('Reject wrong input features', lambda f: rejects(f,[1,2],[[1]],[0])),
        ('Reject wrong bias', lambda f: rejects(f,[1],[[1]],[0,0])),
        ('Reject empty weights', lambda f: rejects(f,[1],np.empty((0,1)),[])),
        ('Reject NaN weights', lambda f: rejects(f,[1],[[np.nan]],[0])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([4.,5.]),np.zeros((1,2)),np.array([7.]))["output"],np.array([7.]))),
        ('Reject unrepresentable weight scale', lambda f: rejects(f,[1],[[1e-320]],[0])),
    ]
    return run_cases(namespace, 'quantized_linear', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Position zero', lambda f: assert_close(f([[[3,4]]],[[[1,2]]]),(np.array([[[3,4]]]),np.array([[[1,2]]])))),
        ('One-radian rotation', lambda f: assert_close(f([[[1,0],[1,0]]],[[[0,1],[0,1]]]),(np.array([[[1,0],[np.cos(1),np.sin(1)]]]),np.array([[[0,1],[-np.sin(1),np.cos(1)]]])))),
        ('Zero vectors', lambda f: assert_close(f(np.zeros((1,2,2)),np.zeros((1,2,2))),(np.zeros((1,2,2)),np.zeros((1,2,2))))),
        ('Different pair frequencies', lambda f: assert_close(f([[[0,0,0,0],[1,0,1,0]]],np.zeros((1,2,4)))[0][0,1],np.array([np.cos(1),np.sin(1),np.cos(.01),np.sin(.01)]))),
        ('Each batch starts at zero', lambda f: assert_close(f(np.ones((2,1,2)),np.ones((2,1,2))),(np.ones((2,1,2)),np.ones((2,1,2))))),
        ('Preserve norms', lambda f: assert_close(np.sum(f(np.arange(24).reshape(2,3,4),np.ones((2,3,4)))[0]**2,axis=-1),np.sum(np.arange(24).reshape(2,3,4)**2,axis=-1))),
        ('Reject odd dimension', lambda f: rejects(f,np.ones((1,2,3)),np.ones((1,2,3)))),
        ('Reject mismatched shapes', lambda f: rejects(f,np.ones((1,2,2)),np.ones((2,2,2)))),
        ('Reject rank two', lambda f: rejects(f,np.ones((2,2)),np.ones((2,2)))),
        ('Reject empty sequence', lambda f: rejects(f,np.ones((1,0,2)),np.ones((1,0,2)))),
        ('Reject nonfinite values', lambda f: rejects(f,[[[np.nan,0]]],[[[0,0]]])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([[[3.,4.]]]),np.array([[[1.,2.]]])),(np.array([[[3,4]]]),np.array([[[1,2]]]))))
    ]
    return run_cases(namespace, 'apply_rope', cases, mode)

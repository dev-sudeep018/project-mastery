def run_tests(namespace, mode="all"):
    cases = [
        ('One pair', lambda f: assert_close(f([[1,0]],[[1,0]],1),0)),
        ('Two orthogonal matches', lambda f: assert_close(f(np.eye(2),np.eye(2),1),np.log1p(np.exp(-1)))),
        ('Indistinguishable keys', lambda f: assert_close(f([[1,0],[1,0]],[[1,0],[1,0]],1),np.log(2))),
        ('Swapped matches', lambda f: assert_close(f(np.eye(2),np.eye(2)[::-1],1),np.log1p(np.exp(1)))),
        ('Sharp wrong match', lambda f: assert_close(f(np.eye(2),np.eye(2)[::-1],1e-6),1e6)),
        ('Three candidates', lambda f: assert_close(f(np.eye(3),np.eye(3),1),np.log1p(2*np.exp(-1)))),
        ('Reject zero norm', lambda f: rejects(f,[[0,0]],[[1,0]])),
        ('Reject unnormalized rows', lambda f: rejects(f,[[2,0]],[[1,0]])),
        ('Reject shape mismatch', lambda f: rejects(f,np.eye(2),np.eye(3))),
        ('Reject invalid temperature', lambda f: [rejects(f,np.eye(2),np.eye(2),value) for value in (0,1e-7,True,2**4096)]),
        ('Reject empty batch', lambda f: rejects(f,np.empty((0,2)),np.empty((0,2)))),
        ('No mutation', lambda f: assert_close(unchanged(f,np.eye(2),np.eye(2),1),np.log1p(np.exp(-1))))
    ]
    return run_cases(namespace, 'contrastive_loss', cases, mode)

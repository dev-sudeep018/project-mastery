def run_tests(namespace, mode="all"):
    cases = [
        ('Keep one token', lambda f: assert_close(f([1,3,2],1),np.array([0.,1.,0.]))),
        ('Keep two tokens', lambda f: assert_close(f([0,np.log(3),-10],2),np.array([.25,.75,0.]))),
        ('Resolve ties', lambda f: assert_close(f([2,2,2],2),np.array([.5,.5,0.]))),
        ('Temperature changes probabilities', lambda f: assert_close(f([0,np.log(4)],2,2),np.array([1/3,2/3]))),
        ('All candidates', lambda f: assert_close(f(np.zeros(4),4),np.full(4,.25))),
        ('Extreme logits', lambda f: assert_close(f([-1000,1000],2),np.array([0.,1.]))),
        ('Negative logits', lambda f: assert_close(f([-4,-2,-3],1),np.array([0.,1.,0.]))),
        ('Reject invalid k', lambda f: [rejects(f,[1,2],value) for value in (0,3,True,1.5,2**4096)]),
        ('Reject invalid temperature', lambda f: [rejects(f,[1,2],1,value) for value in (0,1e-7,True,2**4096)]),
        ('Reject matrix', lambda f: rejects(f,[[1,2]],1)),
        ('Reject nonfinite logits', lambda f: rejects(f,[np.nan,1],1)),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([1.,3.,2.]),1),np.array([0.,1.,0.])))
    ]
    return run_cases(namespace, 'top_k_distribution', cases, mode)

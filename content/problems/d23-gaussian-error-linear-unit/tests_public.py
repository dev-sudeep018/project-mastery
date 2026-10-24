def run_tests(namespace, mode="all"):
    cases = [
        ('At the origin', lambda f: assert_close(f([0]),np.array([0.]))),
        ('Opposite inputs', lambda f: assert_close(f([-1,1]),np.array([-.158655253931457,.841344746068543]))),
        ('Two-dimensional input', lambda f: assert_close(f([[-2,2]]),np.array([[-.0455002638963584,1.95449973610364]]))),
        ('Gaussian symmetry', lambda f: assert_close(f(np.array([.3,1.7,4]))-f(np.array([-.3,-1.7,-4])),np.array([.3,1.7,4]))),
        ('Large finite tails', lambda f: assert_close(f([-1000,1000]),np.array([0.,1000.]))),
        ('Preserve three axes', lambda f: assert_close(f(np.zeros((2,3,4))),np.zeros((2,3,4)))),
        ('Reject scalar input', lambda f: rejects(f,1)),
        ('Reject empty axis', lambda f: rejects(f,np.empty((1,0)))),
        ('Reject nonfinite input', lambda f: rejects(f,[np.inf])),
        ('Reject boolean values', lambda f: rejects(f,[True])),
        ('Reject oversized values', lambda f: rejects(f,[1e31])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([-1.,1.])),np.array([-.158655253931457,.841344746068543])))
    ]
    return run_cases(namespace, 'gelu', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Zero gate', lambda f: assert_close(f([2],[[3]],[[0]],[[4]]),np.array([0.]))),
        ('Unit gate', lambda f: assert_close(f([1],[[2]],[[1]],[[3]]),np.array([4.38635147178003]))),
        ('Negative gate', lambda f: assert_close(f([-1],[[2]],[[1]],[[3]]),np.array([1.61364852821997]))),
        ('Separate branches', lambda f: assert_close(f([1,2],[[1],[0]],[[0],[1]],[[1]]),np.array([1.76159415595576]))),
        ('Extreme gates', lambda f: assert_close(f(np.array([[-1000.],[1000.]]),[[1]],[[1]],[[1]]),np.array([[0.],[1e6]]))),
        ('Leading dimensions', lambda f: assert_close(f(np.ones((2,3,1)),[[2]],[[0]],[[3]]),np.zeros((2,3,1)))),
        ('Reject mismatched gate', lambda f: rejects(f,[1],[[1]],[[1,2]],[[1]])),
        ('Reject output shape', lambda f: rejects(f,[1],[[1]],[[1]],[[1],[2]])),
        ('Reject empty input', lambda f: rejects(f,np.empty((0,1)),[[1]],[[1]],[[1]])),
        ('Reject nonfinite weights', lambda f: rejects(f,[1],[[np.nan]],[[1]],[[1]])),
        ('Reject scalar input', lambda f: rejects(f,1,[[1]],[[1]],[[1]])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([1.]),np.array([[2.]]),np.array([[1.]]),np.array([[3.]])),np.array([4.38635147178003])))
    ]
    return run_cases(namespace, 'swiglu', cases, mode)

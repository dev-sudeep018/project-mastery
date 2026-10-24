def run_tests(namespace, mode="all"):
    cases = [
        ('Training transition', lambda f: assert_close(f([[1],[3]],[1],[0],[0],[0],True,.5,3),{"output":np.array([[-.5],[.5]]),"running_mean":np.array([1.]),"running_var":np.array([.5])})),
        ('Inference state', lambda f: assert_close(f([[3]],[2],[1],[1],[3],False,.1,1),{"output":np.array([[3.]]),"running_mean":np.array([1.]),"running_var":np.array([3.])})),
        ('One training example', lambda f: assert_close(f([[4]],[2],[5],[0],[2],True,1),{"output":np.array([[5.]]),"running_mean":np.array([4.]),"running_var":np.array([0.])})),
        ('Population variance', lambda f: assert_close(f([[0],[4]],[1],[0],[0],[0],True,1)["running_var"],np.array([4.]))),
        ('Zero momentum preserves state', lambda f: assert_close(f([[1],[3]],[1],[0],[8],[9],True,0)["running_mean"],np.array([8.]))),
        ('Independent features', lambda f: assert_close(f([[1,8],[3,8]],[1,2],[0,5],[0,0],[1,1],True,1,3)["output"],np.array([[-.5,5],[.5,5]]))),
        ('Reject broadcast state', lambda f: rejects(f,[[1,2]],[1],[0,0],[0,0],[1,1])),
        ('Reject negative variance', lambda f: rejects(f,[[1]],[1],[0],[0],[-1])),
        ('Reject numeric mode', lambda f: rejects(f,[[1]],[1],[0],[0],[1],1)),
        ('Reject invalid parameters', lambda f: [rejects(f,[[1]],[1],[0],[0],[1],True,value) for value in (-.1,1.1,2**4096)]),
        ('Reject zero epsilon', lambda f: rejects(f,[[1]],[1],[0],[0],[1],True,.1,0)),
        ('No mutation', lambda f: assert_close(unchanged(f,np.array([[1.],[3.]]),np.ones(1),np.zeros(1),np.zeros(1),np.zeros(1),True,.5,3)["running_mean"],np.array([1.])))
    ]
    return run_cases(namespace, 'batch_norm', cases, mode)

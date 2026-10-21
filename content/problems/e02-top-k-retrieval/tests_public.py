def run_tests(namespace, mode="all"):
    cases = [
        ("Directional ranking", lambda f: assert_close(f([1,0],[[0,1],[1,0],[-1,0]],2), [1,0])),
        ("Stable ties", lambda f: assert_close(f([1,0],[[1,0],[2,0],[3,0]],2), [0,1])),
        ("Zero results", lambda f: assert_close(f([1],[[1]],0), [])),
        ("Zero query", lambda f: assert_close(f([0,0],[[1,2],[0,0],[-1,2]],3), [0,1,2])),
        ("Zero document", lambda f: assert_close(f([1,0],[[-1,0],[0,0],[1,0]],3), [2,1,0])),
        ("Extreme finite vectors", lambda f: assert_close(f([1e308,0],[[1e-300,0],[0,1e308]],2), [0,1])),
        ("Inputs unchanged", lambda f: assert_close(unchanged(f,np.array([1.,0.]),np.array([[0.,1.],[1.,0.]]),1), [1])),
        ("Wrong feature count", lambda f: rejects(f,[1,2],[[1]],1)),
        ("Empty corpus", lambda f: rejects(f,[1],np.empty((0,1)),0)),
        ("Excess k", lambda f: rejects(f,[1],[[1]],2)),
        ("Boolean k", lambda f: rejects(f,[1],[[1]],True)),
        ("Non-finite vector", lambda f: rejects(f,[1],[[float("inf")]],1)),
    ]
    return run_cases(namespace, 'top_k_cosine', cases, mode)

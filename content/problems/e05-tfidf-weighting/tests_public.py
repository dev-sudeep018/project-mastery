def run_tests(namespace, mode="all"):
    cases = [
        ('Equally common terms', lambda f: assert_close(f([[1,1],[1,1]]), {"idf":np.ones(2),"weights":np.full((2,2),1/np.sqrt(2))})),
        ('Separate terms', lambda f: assert_close(f([[2,0],[0,1]]), {"idf":np.full(2,1+np.log(1.5)),"weights":np.eye(2)})),
        ('Empty document and absent term', lambda f: assert_close(f([[0,0],[1,0]]), {"idf":np.array([1+np.log(1.5),1+np.log(3)]),"weights":np.array([[0.,0.],[1.,0.]])})),
        ('Document frequency not total frequency', lambda f: assert_close(f([[10,1],[0,1]])["idf"], np.array([1+np.log(1.5),1.]))),
        ('Weight before normalization', lambda f: assert_close(f([[1,1],[0,1]])["weights"][0], np.array([1+np.log(1.5),1.])/np.sqrt((1+np.log(1.5))**2+1))),
        ('Whole zero corpus', lambda f: assert_close(f([[0,0],[0,0]])["weights"], np.zeros((2,2)))),
        ('One term', lambda f: assert_close(f([[5],[0],[2]])["weights"], np.array([[1.],[0.],[1.]]))),
        ('No input mutation', lambda f: assert_close(unchanged(f, np.array([[2,0],[0,1]]))["weights"], np.eye(2))),
        ('Reject vector', lambda f: rejects(f, [1,2])),
        ('Reject empty documents', lambda f: rejects(f, np.empty((0,2)))),
        ('Reject empty vocabulary', lambda f: rejects(f, np.empty((2,0)))),
        ('Reject negative counts', lambda f: rejects(f, [[-1,2]])),
        ('Reject fractional counts', lambda f: rejects(f, [[.5,1]])),
        ('Reject nonfinite counts', lambda f: rejects(f, [[np.nan,1]])),
    ]
    return run_cases(namespace, 'tfidf_weights', cases, mode)

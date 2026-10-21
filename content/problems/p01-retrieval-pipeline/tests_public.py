def run_tests(namespace, mode="all"):
    cases = [
        ("Vector baseline", lambda f: assert_close(f(["a","b"],[[1,0],[0,1]],[[1,0]],[["b","a"]],[["b"]],1,1), {"rankings":[["a"]],"recall":0.,"mrr":0.})),
        ("Keyword baseline", lambda f: assert_close(f(["a","b"],[[1,0],[0,1]],[[1,0]],[["b","a"]],[["b"]],1,0), {"rankings":[["b"]],"recall":1.,"mrr":1.})),
        ("Retrieve both", lambda f: assert_close(f(["a","b"],[[1,0],[0,1]],[[1,0]],[["b","a"]],[["b"]],2,1), {"rankings":[["a","b"]],"recall":1.,"mrr":.5})),
        ("Fusion tie order", lambda f: assert_close(f(["a","b"],[[1,0],[0,1]],[[1,0]],[["b","a"]],[["a"]],1,.5), {"rankings":[["a"]],"recall":1.,"mrr":1.})),
        ("ID tie rather than row order", lambda f: assert_close(f(["b","a"],[[1],[1]],[[1]],[[]],[["a"]],1,1), {"rankings":[["a"]],"recall":1.,"mrr":1.})),
        ("Multiple queries and labels", lambda f: assert_close(f(["a","b"],[[1,0],[0,1]],[[1,0],[0,1]],[[],[]],[["a","b"],["b"]],1,1), {"rankings":[["a"],["b"]],"recall":.75,"mrr":1.})),
        ("Inputs unchanged", lambda f: assert_close(unchanged(f,["a"],np.array([[1.]]),np.array([[1.]]),[["a","a"]],[[]],1), {"rankings":[["a"]],"recall":0.,"mrr":0.})),
        ("Duplicate document IDs", lambda f: rejects(f,["a","a"],[[1],[2]],[[1]],[[]],[[]],1)),
        ("Unknown lexical ID", lambda f: rejects(f,["a"],[[1]],[[1]],[["x"]],[[]],1)),
        ("Invalid weight", lambda f: rejects(f,["a"],[[1]],[[1]],[[]],[[]],1,1.5)),
        ("Invalid k", lambda f: rejects(f,["a"],[[1]],[[1]],[[]],[[]],0)),
        ("Non-finite query", lambda f: rejects(f,["a"],[[1]],[[float("inf")]],[[]],[[]],1)),
        ("Query count mismatch", lambda f: rejects(f,["a"],[[1]],[[1]],[],[[]],1)),
    ]
    return run_cases(namespace, 'retrieval_pipeline', cases, mode)

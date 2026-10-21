def run_tests(namespace, mode="all"):
    cases = [
        ("Two queries", lambda f: assert_close(f([["a","b"],["c","d"]],[["a","x"],["d"]],2), {"recall":.75,"mrr":.75})),
        ("No hit", lambda f: assert_close(f([["a"]],[["b"]],1), {"recall":0.,"mrr":0.})),
        ("Deduplicate before cutoff", lambda f: assert_close(f([["x","x","a"]],[["a"]],2), {"recall":1.,"mrr":.5})),
        ("Duplicate labels", lambda f: assert_close(f([["a"]],[["a","a"]],1), {"recall":1.,"mrr":1.})),
        ("Cutoff excludes hit", lambda f: assert_close(f([["x","a"]],[["a"]],1), {"recall":0.,"mrr":0.})),
        ("Empty query set", lambda f: assert_close(f([],[],1), {"recall":0.,"mrr":0.})),
        ("Unlabelled query counts zero", lambda f: assert_close(f([["a"],["b"]],[[],["b"]],1), {"recall":.5,"mrr":.5})),
        ("Inputs unchanged", lambda f: assert_close(unchanged(f,[["a","a"]],[["a"]],2), {"recall":1.,"mrr":1.})),
        ("Unequal query counts", lambda f: rejects(f,[["a"]],[],1)),
        ("Zero k", lambda f: rejects(f,[],[],0)),
        ("Boolean k", lambda f: rejects(f,[],[],True)),
        ("Non-string ID", lambda f: rejects(f,[[1]],[["a"]],1)),
    ]
    return run_cases(namespace, 'retrieval_metrics', cases, mode)

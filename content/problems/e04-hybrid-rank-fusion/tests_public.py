def run_tests(namespace, mode="all"):
    cases = [
        ("Agreement", lambda f: assert_close(f([["a","b"],["b","c"]],1), ["b","a","c"])),
        ("Lexical tie break", lambda f: assert_close(f([["b"],["a"]]), ["a","b"])),
        ("Weighted methods", lambda f: assert_close(f([["a"],["b"]],weights=[1,2]), ["b","a"])),
        ("Duplicate ranks removed", lambda f: assert_close(f([["a","a","b"],["b"]],1), ["b","a"])),
        ("Limit", lambda f: assert_close(f([["a","b"]],limit=1), ["a"])),
        ("Zero limit", lambda f: assert_close(f([["a"]],limit=0), [])),
        ("Empty rankings", lambda f: assert_close(f([]), [])),
        ("Inputs unchanged", lambda f: assert_close(unchanged(f,[["a","a","b"]]), ["a","b"])),
        ("Invalid constant", lambda f: rejects(f,[["a"]],0)),
        ("Mismatched weights", lambda f: rejects(f,[["a"]],weights=[])),
        ("Negative weight", lambda f: rejects(f,[["a"]],weights=[-1])),
        ("All zero weights", lambda f: rejects(f,[["a"]],weights=[0])),
        ("Non-finite weight", lambda f: rejects(f,[["a"]],weights=[float("inf")])),
        ("Boolean limit", lambda f: rejects(f,[["a"]],limit=True)),
    ]
    return run_cases(namespace, 'reciprocal_rank_fusion', cases, mode)

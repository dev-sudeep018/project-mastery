def run_tests(namespace, mode="all"):
    cases = [
        ('Ideal ordering', lambda f: assert_close(f(["a","b"], {"a":3,"b":1}, 2), 1.)),
        ('Weak first result', lambda f: assert_close(f(["b","a"], {"a":3,"b":1}, 1), 1/3)),
        ('No positive judgments', lambda f: assert_close(f(["a"], {"a":0}, 3), 0.)),
        ('Discount reversed ranking', lambda f: assert_close(f(["b","a"], {"a":3,"b":1}, 2), (1+3/math.log2(3))/(3+1/math.log2(3)))),
        ('Missing best document affects ideal', lambda f: assert_close(f(["b"], {"a":3,"b":1}, 2), 1/(3+1/math.log2(3)))),
        ('Deduplicate before cutoff', lambda f: assert_close(f(["b","b","a"], {"a":3,"b":1}, 2), (1+3/math.log2(3))/(3+1/math.log2(3)))),
        ('Unjudged ID occupies a rank', lambda f: assert_close(f(["x","a"], {"a":3}, 2), 1/math.log2(3))),
        ('Empty ranking', lambda f: assert_close(f([], {"a":3}, 2), 0.)),
        ('Empty judgments', lambda f: assert_close(f(["a"], {}, 2), 0.)),
        ('Zero cutoff', lambda f: assert_close(f(["a"], {"a":3}, 0), 0.)),
        ('No input mutation', lambda f: assert_close(unchanged(f, ["b","a"], {"a":3,"b":1}, 1), 1/3)),
        ('Reject invalid grade', lambda f: rejects(f, ["a"], {"a":-1}, 1)),
        ('Reject nonfinite grade', lambda f: rejects(f, ["a"], {"a":np.inf}, 1)),
        ('Reject grade above range', lambda f: rejects(f, ["a"], {"a":6}, 1)),
        ('Reject string grade', lambda f: rejects(f, ["a"], {"a":"3"}, 1)),
        ('Reject malformed ID', lambda f: rejects(f, [1], {"a":3}, 1)),
        ('Reject negative cutoff', lambda f: rejects(f, ["a"], {"a":3}, -1)),
        ('Reject boolean cutoff', lambda f: rejects(f, ["a"], {"a":3}, True)),
    ]
    return run_cases(namespace, 'ndcg_at_k', cases, mode)

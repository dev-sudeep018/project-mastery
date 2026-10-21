def run_tests(namespace, mode="all"):
    cases = [
        ("Uncertain predictions", lambda f: assert_close(f([0,1], [0,0]), math.log(2))),
        ("Confident and correct", lambda f: assert_close(f([0,1], [-1000,1000]), 0.)),
        ("Confident and wrong", lambda f: assert_close(f([1,0], [-1000,1000]), 1000.)),
        ("Moderate correct prediction", lambda f: assert_close(f([1], [2]), math.log1p(math.exp(-2)))),
        ("Mixed targets", lambda f: assert_close(f([1,0], [2,2]), 1 + math.log1p(math.exp(-2)))),
        ("Extreme representable losses", lambda f: assert_close(f([0,0], [1e308,1e308]), 1e308)),
        ("Inputs remain unchanged", lambda f: assert_close(unchanged(f, np.array([0.,1.]), np.array([0.,0.])), math.log(2))),
        ("Non-binary targets", lambda f: rejects(f, [.5], [0])),
        ("Empty batch", lambda f: rejects(f, [], [])),
        ("Wrong dimensions", lambda f: rejects(f, [[0,1]], [[0,0]])),
        ("Mismatched lengths", lambda f: rejects(f, [0,1], [0])),
        ("Non-finite logits", lambda f: rejects(f, [1], [float("inf")])),
    ]
    return run_cases(namespace, 'binary_cross_entropy', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Short padded sequence', lambda f: assert_close(f([2], 3), np.array([[[True,False,False],[True,True,False],[False,False,False]]]))),
        ('Empty sequence is fully masked', lambda f: assert_close(f([0], 2), np.zeros((1,2,2),dtype=bool))),
        ('Mixed batch lengths', lambda f: assert_close(f([1,2], 2), np.array([[[True,False],[False,False]],[[True,False],[True,True]]]))),
        ('Full causal mask', lambda f: assert_close(f([3], 3), np.array([[[True,False,False],[True,True,False],[True,True,True]]]))),
        ('One position', lambda f: assert_close(f([1,0], 1), np.array([[[True]],[[False]]]))),
        ('Reject length exceeds padding', lambda f: rejects(f, [3], 2)),
        ('Reject negative length', lambda f: rejects(f, [-1], 2)),
        ('Reject fractional length', lambda f: rejects(f, [1.5], 2)),
        ('Reject empty batch', lambda f: rejects(f, [], 2)),
        ('Reject boolean padded length', lambda f: rejects(f, [1], True)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([2]), 3), np.array([[[True,False,False],[True,True,False],[False,False,False]]]))),
    ]
    return run_cases(namespace, 'causal_padding_mask', cases, mode)

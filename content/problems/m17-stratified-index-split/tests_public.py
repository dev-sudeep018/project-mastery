def run_tests(namespace, mode="all"):
    cases = [
        ('Interleaved classes', lambda f: assert_close(f([0,1,0,1,0,1], .5), {'train':[0,1], 'test':[2,3,4,5]})),
        ('Protect tiny test split', lambda f: assert_close(f([0,0,1,1], .99), {'train':[0,2], 'test':[1,3]})),
        ('Protect tiny training split', lambda f: assert_close(f([0,0,0,0], .01), {'train':[0], 'test':[1,2,3]})),
        ('Unequal class sizes', lambda f: assert_close(f([4,4,4,4,9,9], .75), {'train':[0,1,2,4], 'test':[3,5]})),
        ('Single observed class', lambda f: assert_close(f([7,7,7,7], .5), {'train':[0,1], 'test':[2,3]})),
        ('Reject singleton class', lambda f: rejects(f, [0,0,1], .5)),
        ('Reject fraction one', lambda f: rejects(f, [0,0], 1)),
        ('Reject fraction zero', lambda f: rejects(f, [0,0], 0)),
        ('Reject fractional label', lambda f: rejects(f, [.5,.5], .5)),
        ('Reject empty labels', lambda f: rejects(f, [], .5)),
        ('Reject non-finite fraction', lambda f: rejects(f, [0,0], np.nan)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([0, 1, 0, 1, 0, 1]), 0.5), {'train':[0,1], 'test':[2,3,4,5]})),
    ]
    return run_cases(namespace, 'stratified_indices', cases, mode)

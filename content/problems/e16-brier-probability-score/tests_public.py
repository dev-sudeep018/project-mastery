def run_tests(namespace, mode="all"):
    cases = [
        ('Perfect probabilities', lambda f: assert_close(f([0,1], [0,1]), 0.)),
        ('Confidently wrong', lambda f: assert_close(f([0,1], [1,0]), 1.)),
        ('Uncertain forecasts', lambda f: assert_close(f([0,1,1], [.5,.5,.5]), .25)),
        ('No thresholding', lambda f: assert_close(f([0,1], [.2,.8]), .04)),
        ('Mean across observations', lambda f: assert_close(f([1,0,1], [1,.5,0]), 5/12)),
        ('Single observation', lambda f: assert_close(f([0], [.9]), .81)),
        ('Reject probability above one', lambda f: rejects(f, [1], [1.1])),
        ('Reject negative probability', lambda f: rejects(f, [0], [-.1])),
        ('Reject nonbinary outcome', lambda f: rejects(f, [2], [.5])),
        ('Reject empty observations', lambda f: rejects(f, [], [])),
        ('Reject length mismatch', lambda f: rejects(f, [0,1], [.5])),
        ('Reject non-finite forecast', lambda f: rejects(f, [0], [np.nan])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([0, 1]), np.array([0, 1])), 0.)),
    ]
    return run_cases(namespace, 'brier_score', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Two occupied bins', lambda f: assert_close(f([0,0,1,1], [.1,.3,.7,.9], 2), {'counts':np.array([2,2]),'mean_probability':np.array([.2,.8]),'positive_fraction':np.array([0,1]),'ece':.2})),
        ('Boundary and probability one', lambda f: assert_close(f([0,1,1], [0,.5,1], 2), {'counts':np.array([1,2]),'mean_probability':np.array([0,.75]),'positive_fraction':np.array([0,1]),'ece':1/6})),
        ('Empty bins', lambda f: assert_close(f([1], [.8], 4), {'counts':np.array([0,0,0,1]),'mean_probability':np.array([0,0,0,.8]),'positive_fraction':np.array([0,0,0,1]),'ece':.2})),
        ('One bin with zero gap', lambda f: assert_close(f([0,1], [.2,.8], 1), {'counts':np.array([2]),'mean_probability':np.array([.5]),'positive_fraction':np.array([.5]),'ece':0.})),
        ('Unequal bin occupancy', lambda f: assert_close(f([0,0,0,0], [0,0,0,1], 2), {'counts':np.array([3,1]),'mean_probability':np.array([0,1]),'positive_fraction':np.array([0,0]),'ece':.25})),
        ('Reject zero bins', lambda f: rejects(f, [0], [.5], 0)),
        ('Reject boolean bins', lambda f: rejects(f, [0], [.5], True)),
        ('Reject out-of-range probability', lambda f: rejects(f, [0], [1.1], 2)),
        ('Reject nonbinary outcome', lambda f: rejects(f, [2], [.5], 2)),
        ('Reject empty observations', lambda f: rejects(f, [], [], 2)),
        ('Reject non-finite probability', lambda f: rejects(f, [0], [np.nan], 2)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([0, 0, 1, 1]), np.array([0.1, 0.3, 0.7, 0.9]), 2), {'counts':np.array([2,2]),'mean_probability':np.array([.2,.8]),'positive_fraction':np.array([0,1]),'ece':.2})),
    ]
    return run_cases(namespace, 'calibration_bins', cases, mode)

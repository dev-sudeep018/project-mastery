def run_tests(namespace, mode="all"):
    cases = [
        ('Perfect ordering', lambda f: assert_close(f([0,1,0,1], [.1,.9,.2,.8]), 1.)),
        ('All scores tied', lambda f: assert_close(f([0,1,0], [3,3,3]), .5)),
        ('Partially correct order', lambda f: assert_close(f([0,1,0,1], [0,1,2,3]), .75)),
        ('Reversed ordering', lambda f: assert_close(f([1,1,0,0], [-4,-3,-2,-1]), 0.)),
        ('One win and one tie', lambda f: assert_close(f([1,0,0], [2,1,2]), .75)),
        ('Class imbalance', lambda f: assert_close(f([0,0,0,1], [1,2,3,4]), 1.)),
        ('Reject only positives', lambda f: rejects(f, [1,1], [1,2])),
        ('Reject only negatives', lambda f: rejects(f, [0,0], [1,2])),
        ('Reject nonbinary labels', lambda f: rejects(f, [0,2], [1,2])),
        ('Reject different lengths', lambda f: rejects(f, [0,1], [1])),
        ('Reject non-finite score', lambda f: rejects(f, [0,1], [0,np.inf])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([0, 1, 0, 1]), np.array([0.1, 0.9, 0.2, 0.8])), 1.)),
    ]
    return run_cases(namespace, 'pairwise_auc', cases, mode)

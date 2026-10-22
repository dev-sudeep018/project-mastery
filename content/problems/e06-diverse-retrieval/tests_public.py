def run_tests(namespace, mode="all"):
    cases = [
        ('Avoid a near duplicate', lambda f: assert_close(f([.9,.85,.6], [[1,.95,.1],[.95,1,.2],[.1,.2,1]], 2, .5), [0,2])),
        ('Relevance alone', lambda f: assert_close(f([.9,.85,.6], [[1,.95,.1],[.95,1,.2],[.1,.2,1]], 2, 1), [0,1])),
        ('Stable ties', lambda f: assert_close(f([.5,.5], [[1,0],[0,1]], 2, .5), [0,1])),
        ('Zero cutoff', lambda f: assert_close(f([.8], [[1]], 0, .5), [])),
        ('Diversity after relevance seed', lambda f: assert_close(f([.2,.9,.1], [[1,.8,.2],[.8,1,.1],[.2,.1,1]], 2, 0), [1,2])),
        ('Compare to the whole selected set', lambda f: assert_close(f([1,.9,.8,.7], [[1,.9,.1,.5],[.9,1,0,.2],[.1,0,1,.5],[.5,.2,.5,1]], 3, .5), [0,2,3])),
        ('No duplicate selections', lambda f: assert_close(f([.5,.5,.5], np.ones((3,3)), 3, 0), [0,1,2])),
        ('No input mutation', lambda f: assert_close(unchanged(f, np.array([.9,.8]), np.eye(2), 2, .5), [0,1])),
        ('Reject empty candidates', lambda f: rejects(f, [], np.empty((0,0)), 0, .5)),
        ('Reject wrong matrix', lambda f: rejects(f, [.5,.4], [[1]], 1, .5)),
        ('Reject asymmetric scores', lambda f: rejects(f, [.5,.4], [[1,.2],[.3,1]], 1, .5)),
        ('Reject invalid diagonal', lambda f: rejects(f, [.5], [[0]], 1, .5)),
        ('Reject negative score', lambda f: rejects(f, [-.5], [[1]], 1, .5)),
        ('Reject nonfinite similarity', lambda f: rejects(f, [.5], [[np.nan]], 1, .5)),
        ('Reject oversized cutoff', lambda f: rejects(f, [.5], [[1]], 2, .5)),
        ('Reject boolean cutoff', lambda f: rejects(f, [.5], [[1]], True, .5)),
        ('Reject invalid weight', lambda f: rejects(f, [.5], [[1]], 1, 1.1)),
        ('Reject vector weight', lambda f: rejects(f, [.5], [[1]], 1, [.5])),
    ]
    return run_cases(namespace, 'mmr_select', cases, mode)

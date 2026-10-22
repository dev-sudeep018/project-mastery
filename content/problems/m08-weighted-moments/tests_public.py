def run_tests(namespace, mode="all"):
    cases = [
        ('Reliability changes the mean', lambda f: assert_close(f([1, 5], [3, 1]), {'mean':2., 'variance':3.})),
        ('Ignore zero-weight outlier', lambda f: assert_close(f([2, 100], [1, 0]), {'mean':2., 'variance':0.})),
        ('Equal weights', lambda f: assert_close(f([-2, 0, 2], [1, 1, 1]), {'mean':0., 'variance':8/3})),
        ('Rescaled weights', lambda f: assert_close(f([1, 5], [30, 10]), {'mean':2., 'variance':3.})),
        ('One observation', lambda f: assert_close(f([7], [.2]), {'mean':7., 'variance':0.})),
        ('Translated observations', lambda f: assert_close(f([1001, 1005], [3, 1]), {'mean':1002., 'variance':3.})),
        ('Reject all-zero weights', lambda f: rejects(f, [1, 2], [0, 0])),
        ('Reject negative weight', lambda f: rejects(f, [1, 2], [2, -1])),
        ('Reject unequal lengths', lambda f: rejects(f, [1, 2], [1])),
        ('Reject empty vectors', lambda f: rejects(f, [], [])),
        ('Reject non-finite input', lambda f: rejects(f, [np.nan], [1])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([1, 5]), np.array([3, 1])), {'mean':2., 'variance':3.})),
    ]
    return run_cases(namespace, 'weighted_moments', cases, mode)

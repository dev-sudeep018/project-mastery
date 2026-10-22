def run_tests(namespace, mode="all"):
    cases = [
        ('Bias-corrected first step', lambda f: assert_close(f([1,2], [2,-4], [0,0], [0,0], 1, .3, .5, .5, 1), {'parameters':np.array([.8,2.24]),'m':np.array([1,-2]),'v':np.array([2,8])})),
        ('Second step with constant gradient', lambda f: assert_close(f([1], [2], [1], [2], 2, .3, .5, .5, 1), {'parameters':np.array([.8]),'m':np.array([1.5]),'v':np.array([3])})),
        ('Zero gradient and moments', lambda f: assert_close(f([3], [0], [0], [0], 1, .1, .9, .99, .001), {'parameters':np.array([3]),'m':np.array([0]),'v':np.array([0])})),
        ('No moment history', lambda f: assert_close(f([1], [-2], [100], [100], 3, .3, 0, 0, 1), {'parameters':np.array([1.2]),'m':np.array([-2]),'v':np.array([4])})),
        ('Epsilon outside square root', lambda f: assert_close(f([1], [3], [0], [0], 1, 1, 0, 0, 1), {'parameters':np.array([.25]),'m':np.array([3]),'v':np.array([9])})),
        ('Reject step zero', lambda f: rejects(f, [1], [1], [0], [0], 0, .1, .9, .99, .001)),
        ('Reject negative second moment', lambda f: rejects(f, [1], [1], [0], [-1], 1, .1, .9, .99, .001)),
        ('Reject beta at one', lambda f: rejects(f, [1], [1], [0], [0], 1, .1, 1, .99, .001)),
        ('Reject epsilon zero', lambda f: rejects(f, [1], [1], [0], [0], 1, .1, .9, .99, 0)),
        ('Reject state mismatch', lambda f: rejects(f, [1,2], [1], [0], [0], 1, .1, .9, .99, .001)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([1, 2]), np.array([2, -4]), np.array([0, 0]), np.array([0, 0]), 1, 0.3, 0.5, 0.5, 1), {'parameters':np.array([.8,2.24]),'m':np.array([1,-2]),'v':np.array([2,8])})),
    ]
    return run_cases(namespace, 'adam_step', cases, mode)

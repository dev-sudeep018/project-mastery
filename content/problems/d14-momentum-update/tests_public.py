def run_tests(namespace, mode="all"):
    cases = [
        ('First step', lambda f: assert_close(f([1,2], [2,-4], [0,0], .1, .9), {'parameters':np.array([.8,2.4]),'velocity':np.array([2,-4])})),
        ('History moves without a new gradient', lambda f: assert_close(f([1], [0], [2], .1, .5), {'parameters':np.array([.9]),'velocity':np.array([1])})),
        ('Opposite gradients cancel', lambda f: assert_close(f([1], [-1], [2], .1, .5), {'parameters':np.array([1]),'velocity':np.array([0])})),
        ('No momentum', lambda f: assert_close(f([3], [2], [100], .25, 0), {'parameters':np.array([2.5]),'velocity':np.array([2])})),
        ('History reinforces gradient', lambda f: assert_close(f([2], [1], [2], .5, .5), {'parameters':np.array([1]),'velocity':np.array([2])})),
        ('Reject state shape mismatch', lambda f: rejects(f, [1,2], [1], [0,0], .1, .9)),
        ('Reject beta one', lambda f: rejects(f, [1], [1], [0], .1, 1)),
        ('Reject negative rate', lambda f: rejects(f, [1], [1], [0], -.1, .9)),
        ('Reject empty state', lambda f: rejects(f, [], [], [], .1, .9)),
        ('Reject non-finite state', lambda f: rejects(f, [1], [np.inf], [0], .1, .9)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([1, 2]), np.array([2, -4]), np.array([0, 0]), 0.1, 0.9), {'parameters':np.array([.8,2.4]),'velocity':np.array([2,-4])})),
    ]
    return run_cases(namespace, 'momentum_step', cases, mode)

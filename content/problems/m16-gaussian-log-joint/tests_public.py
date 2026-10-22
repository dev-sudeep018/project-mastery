def run_tests(namespace, mode="all"):
    cases = [
        ('Equal priors', lambda f: assert_close(f([[0]], [.5,.5], [[0],[2]], [[1],[1]]), {'log_joint':np.array([[-1.612085713764618,-3.612085713764618]]),'predictions':np.array([0])})),
        ('Prior decides identical likelihoods', lambda f: assert_close(f([[0]], [.25,.75], [[0],[0]], [[1],[1]]), {'log_joint':np.array([[-2.305232894324563,-1.206620605656454]]),'predictions':np.array([1])})),
        ('Variance changes peak density', lambda f: assert_close(f([[0]], [.5,.5], [[0],[0]], [[1],[4]]), {'log_joint':np.array([[-1.612085713764618,-2.305232894324563]]),'predictions':np.array([0])})),
        ('Two independent features', lambda f: assert_close(f([[0,0]], [1], [[0,0]], [[1,1]]), {'log_joint':np.array([[-1.8378770664093453]]),'predictions':np.array([0])})),
        ('Exact class tie', lambda f: assert_close(f([[1]], [.5,.5], [[0],[2]], [[1],[1]]), {'log_joint':np.array([[-2.112085713764618,-2.112085713764618]]),'predictions':np.array([0])})),
        ('Reject zero variance', lambda f: rejects(f, [[0]], [1], [[0]], [[0]])),
        ('Reject unnormalized priors', lambda f: rejects(f, [[0]], [.4], [[0]], [[1]])),
        ('Reject zero prior', lambda f: rejects(f, [[0]], [1,0], [[0],[1]], [[1],[1]])),
        ('Reject feature mismatch', lambda f: rejects(f, [[0,1]], [1], [[0]], [[1]])),
        ('Reject non-finite observation', lambda f: rejects(f, [[np.inf]], [1], [[0]], [[1]])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[0]]), np.array([0.5, 0.5]), np.array([[0], [2]]), np.array([[1], [1]])), {'log_joint':np.array([[-1.612085713764618,-3.612085713764618]]),'predictions':np.array([0])})),
    ]
    return run_cases(namespace, 'gaussian_log_joint', cases, mode)

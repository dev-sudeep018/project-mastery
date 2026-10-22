def run_tests(namespace, mode="all"):
    cases = [
        ('Positive relationship', lambda f: assert_close(f([[1,2], [3,4]]), np.array([[2.,2.],[2.,2.]]))),
        ('Opposing movement', lambda f: assert_close(f([[0,2], [1,1], [2,0]]), np.array([[1.,-1.],[-1.,1.]]))),
        ('One feature remains a matrix', lambda f: assert_close(f([[1], [3], [5]]), np.array([[4.]]))),
        ('Constant features', lambda f: assert_close(f([[2,3],[2,3],[2,3]]), np.zeros((2,2)))),
        ('Translation invariance', lambda f: assert_close(f([[101,-8],[103,-6]]), np.array([[2.,2.],[2.,2.]]))),
        ('Independent axes', lambda f: assert_close(f([[-1,0],[1,0],[0,-1],[0,1]]), np.eye(2)*2/3)),
        ('Reject one observation', lambda f: rejects(f, [[1,2]])),
        ('Reject vector input', lambda f: rejects(f, [1,2])),
        ('Reject no features', lambda f: rejects(f, np.empty((3,0)))),
        ('Reject non-finite values', lambda f: rejects(f, [[1],[np.inf]])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[1, 2], [3, 4]])), np.array([[2.,2.],[2.,2.]]))),
    ]
    return run_cases(namespace, 'sample_covariance', cases, mode)

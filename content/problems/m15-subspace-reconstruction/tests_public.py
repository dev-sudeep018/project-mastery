def run_tests(namespace, mode="all"):
    cases = [
        ('Discard second coordinate', lambda f: assert_close(f([[3,8],[5,9]], [1,2], [[1,0]]), {'scores':np.array([[2],[4]]),'reconstruction':np.array([[3,2],[5,2]])})),
        ('Complete basis', lambda f: assert_close(f([[2,3]], [1,1], [[0,1],[1,0]]), {'scores':np.array([[2,1]]),'reconstruction':np.array([[2,3]])})),
        ('Negative direction', lambda f: assert_close(f([[4]], [1], [[-1]]), {'scores':np.array([[-3]]),'reconstruction':np.array([[4]])})),
        ('Mean maps to zero', lambda f: assert_close(f([[1,2]], [1,2], [[1,0]]), {'scores':np.zeros((1,1)),'reconstruction':np.array([[1,2]])})),
        ('Supplied mean stays fixed', lambda f: assert_close(f([[10,0]], [0,0], [[1,0]]), {'scores':np.array([[10]]),'reconstruction':np.array([[10,0]])})),
        ('Reject non-unit direction', lambda f: rejects(f, [[1,2]], [0,0], [[2,0]])),
        ('Reject duplicate directions', lambda f: rejects(f, [[1,2]], [0,0], [[1,0],[1,0]])),
        ('Reject mean width', lambda f: rejects(f, [[1,2]], [0], [[1,0]])),
        ('Reject empty basis', lambda f: rejects(f, [[1,2]], [0,0], np.empty((0,2)))),
        ('Reject non-finite observation', lambda f: rejects(f, [[np.nan,2]], [0,0], [[1,0]])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([[3, 8], [5, 9]]), np.array([1, 2]), np.array([[1, 0]])), {'scores':np.array([[2],[4]]),'reconstruction':np.array([[3,2],[5,2]])})),
    ]
    return run_cases(namespace, 'project_reconstruct', cases, mode)

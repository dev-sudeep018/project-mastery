def run_tests(namespace, mode="all"):
    cases = [
        ('Skip oversized best passage', lambda f: assert_close(f([8,3,2], [10,8,7], 5), [1,2])),
        ('Relevance beats score per token', lambda f: assert_close(f([5,2,2], [9,6,5], 5), [0])),
        ('Stable score ties', lambda f: assert_close(f([3,3,2], [5,5,5], 5), [0,2])),
        ('Zero budget', lambda f: assert_close(f([1,2], [3,4], 0), [])),
        ('Output in score order', lambda f: assert_close(f([1,1,1], [2,5,3], 3), [1,2,0])),
        ('Exact fit', lambda f: assert_close(f([4], [1], 4), [0])),
        ('Reject zero cost', lambda f: rejects(f, [0], [1], 2)),
        ('Reject fractional cost', lambda f: rejects(f, [1.5], [1], 2)),
        ('Reject negative score', lambda f: rejects(f, [1], [-1], 2)),
        ('Reject negative budget', lambda f: rejects(f, [1], [1], -1)),
        ('Reject mismatched lengths', lambda f: rejects(f, [1,2], [1], 2)),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([8, 3, 2]), np.array([10, 8, 7]), 5), [1,2])),
    ]
    return run_cases(namespace, 'select_context', cases, mode)

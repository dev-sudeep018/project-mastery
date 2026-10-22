def run_tests(namespace, mode="all"):
    cases = [
        ('Weighted repeated words', lambda f: assert_close(f([['a','b'],['a','b','c']], [3,2]), {('a','b'):5,('b','c'):2})),
        ('Overlapping pair observations', lambda f: assert_close(f([['a','a','a']], [2]), {('a','a'):4})),
        ('Respect word boundaries', lambda f: assert_close(f([['a'],['b']], [10,10]), {})),
        ('Zero frequency omitted', lambda f: assert_close(f([['a','b'],['b','c']], [0,1]), {('b','c'):1})),
        ('Token boundaries stay distinct', lambda f: assert_close(f([['ab','c'],['a','bc']], [1,1]), {('ab','c'):1,('a','bc'):1})),
        ('Empty word', lambda f: assert_close(f([[]], [2]), {})),
        ('Reject mismatched frequencies', lambda f: rejects(f, [['a']], [1,2])),
        ('Reject negative frequency', lambda f: rejects(f, [['a','b']], [-1])),
        ('Reject empty token', lambda f: rejects(f, [['']], [1])),
        ('Reject fractional frequency', lambda f: rejects(f, [['a']], [.5])),
        ("No input mutation", lambda f: assert_close(unchanged(f, [['a', 'b'], ['a', 'b', 'c']], np.array([3, 2])), {('a','b'):5,('b','c'):2})),
    ]
    return run_cases(namespace, 'bpe_pair_counts', cases, mode)

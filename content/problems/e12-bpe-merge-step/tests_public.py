def run_tests(namespace, mode="all"):
    cases = [
        ('Two separate matches', lambda f: assert_close(f(['a','b','a','b'], ('a','b')), ['ab','ab'])),
        ('Overlapping candidates', lambda f: assert_close(f(['a','a','a'], ('a','a')), ['aa','a'])),
        ('Token boundaries matter', lambda f: assert_close(f(['ab','c'], ('a','b')), ['ab','c'])),
        ('Unmatched suffix', lambda f: assert_close(f(['a','b','a'], ('a','b')), ['ab','a'])),
        ('Empty sequence', lambda f: assert_close(f([], ('a','b')), [])),
        ('Unicode tokens', lambda f: assert_close(f(['你','好','!'], ('你','好')), ['你好','!'])),
        ('Reject empty token', lambda f: rejects(f, [''], ('a','b'))),
        ('Reject one-element pair', lambda f: rejects(f, ['a'], ('a',))),
        ('Reject raw string input', lambda f: rejects(f, 'ab', ('a','b'))),
        ('Reject non-string pair', lambda f: rejects(f, ['a'], ('a',1))),
        ("No input mutation", lambda f: assert_close(unchanged(f, ['a','b','a','b'], ('a','b')), ['ab','ab'])),
    ]
    return run_cases(namespace, 'merge_token_pair', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Position zero', lambda f: assert_close(f(1, 4), np.array([[0,1,0,1]]))),
        ('One frequency pair', lambda f: assert_close(f(2, 2), np.array([[0,1],[0.8414709848078965,0.5403023058681398]]))),
        ('Two frequencies', lambda f: assert_close(f(2, 4), np.array([[0,1,0,1],[0.8414709848078965,0.5403023058681398,0.009999833334166664,0.9999500004166653]]))),
        ('Later position', lambda f: assert_close(f(3, 2), np.array([[0,1],[0.8414709848078965,0.5403023058681398],[0.9092974268256817,-0.4161468365471424]]))),
        ('More channels at origin', lambda f: assert_close(f(1, 6), np.array([[0,1,0,1,0,1]]))),
        ('Reject odd dimensions', lambda f: rejects(f, 2, 3)),
        ('Reject empty sequence', lambda f: rejects(f, 0, 4)),
        ('Reject boolean length', lambda f: rejects(f, True, 4)),
        ('Reject fractional dimension', lambda f: rejects(f, 2, 4.0)),
        ("No input mutation", lambda f: assert_close(unchanged(f, 1, 4), np.array([[0,1,0,1]]))),
    ]
    return run_cases(namespace, 'sinusoidal_positions', cases, mode)

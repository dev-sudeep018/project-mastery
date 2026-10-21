def run_tests(namespace, mode="all"):
    cases = [
        ("Quadratic", lambda f: assert_close(f(lambda x: x*x, 3), 6.)),
        ("Cubic", lambda f: assert_close(f(lambda x: x**3, 2), 12.)),
        ("Sine", lambda f: assert_close(f(np.sin, 0), 1.)),
        ("Negative point", lambda f: assert_close(f(lambda x: x*x, -4), -8.)),
        ("Constant", lambda f: assert_close(f(lambda x: 9., 2), 0.)),
        ("Custom step", lambda f: assert_close(f(lambda x: x**3, 2, .1), 12.01)),
        ("Zero step", lambda f: rejects(f, np.sin, 0, 0)),
        ("Negative step", lambda f: rejects(f, np.sin, 0, -.1)),
        ("Non-finite point", lambda f: rejects(f, np.sin, float("inf"))),
        ("Unrepresentable step", lambda f: rejects(f, np.sin, 1e20, 1e-10)),
        ("Vector function output", lambda f: rejects(f, lambda x: [x,x], 1)),
        ("Non-finite function output", lambda f: rejects(f, lambda x: float("nan"), 1)),
        ("Non-callable function", lambda f: rejects(f, 4, 1)),
    ]
    return run_cases(namespace, 'numerical_derivative', cases, mode)

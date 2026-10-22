def run_tests(namespace, mode="all"):
    cases = [
        ('Center of the gate', lambda f: assert_close(f([0]), {'output':np.array([.5]),'derivative':np.array([.25])})),
        ('Extreme scores', lambda f: assert_close(f([-1000,1000]), {'output':np.array([0.,1.]),'derivative':np.array([0.,0.])})),
        ('Known odds', lambda f: assert_close(f([-np.log(3),np.log(3)]), {'output':np.array([.25,.75]),'derivative':np.array([.1875,.1875])})),
        ('Odds of nine', lambda f: assert_close(f([np.log(9)]), {'output':np.array([.9]),'derivative':np.array([.09])})),
        ('Repeated zeros', lambda f: assert_close(f([0,0,0]), {'output':np.full(3,.5),'derivative':np.full(3,.25)})),
        ('Reject empty vector', lambda f: rejects(f, [])),
        ('Reject matrix input', lambda f: rejects(f, [[0]])),
        ('Reject infinite score', lambda f: rejects(f, [np.inf])),
        ('Reject NaN score', lambda f: rejects(f, [np.nan])),
        ("No input mutation", lambda f: assert_close(unchanged(f, np.array([0])), {'output':np.array([.5]),'derivative':np.array([.25])})),
    ]
    with np.errstate(over="raise"):
        return run_cases(namespace, 'sigmoid_with_gradient', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Mixed decisions', lambda f: assert_close(f([1,0,1,0], [.9,.8,.4,.1], .5), {"tp":1,"fp":1,"tn":1,"fn":1,"precision":.5,"recall":.5,"f1":.5})),
        ('Ties are positive', lambda f: assert_close(f([1,0], [.5,.5], .5), {"tp":1,"fp":1,"tn":0,"fn":0,"precision":.5,"recall":1.,"f1":2/3})),
        ('No predicted positives', lambda f: assert_close(f([1,0], [.2,.1], .9), {"tp":0,"fp":0,"tn":1,"fn":1,"precision":0.,"recall":0.,"f1":0.})),
        ('Perfect classifier', lambda f: assert_close(f([1,0], [1,0], .5)["f1"], 1.)),
        ('No actual positives', lambda f: assert_close(f([0,0], [1,1], .5)["recall"], 0.)),
        ('Threshold zero', lambda f: assert_close(f([1,0], [0,0], 0)["tp"], 1)),
        ('Threshold one', lambda f: assert_close(f([1,0], [1,.9], 1)["fp"], 0)),
        ('No input mutation', lambda f: assert_close(unchanged(f, np.array([1,0]), np.array([.9,.8]), .5)["precision"], .5)),
        ('Reject empty vectors', lambda f: rejects(f, [], [], .5)),
        ('Reject column labels', lambda f: rejects(f, [[1]], [.5], .5)),
        ('Reject length mismatch', lambda f: rejects(f, [1,0], [.5], .5)),
        ('Reject invalid label', lambda f: rejects(f, [2], [.5], .5)),
        ('Reject out of range score', lambda f: rejects(f, [1], [1.1], .5)),
        ('Reject nonfinite score', lambda f: rejects(f, [1], [np.nan], .5)),
        ('Reject vector threshold', lambda f: rejects(f, [1], [.5], [.5])),
        ('Reject out of range threshold', lambda f: rejects(f, [1], [.5], -1)),
    ]
    return run_cases(namespace, 'binary_metrics', cases, mode)

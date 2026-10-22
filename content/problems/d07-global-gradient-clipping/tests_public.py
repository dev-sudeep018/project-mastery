def run_tests(namespace, mode="all"):
    cases = [
        ('One shared scale', lambda f: assert_close(f([[3,4],[0,12]], 6.5), {"norm":13.,"grads":[np.array([1.5,2.]),np.array([0.,6.])]})),
        ('Below the limit', lambda f: assert_close(f([[3,4]], 10), {"norm":5.,"grads":[np.array([3.,4.])]})),
        ('Zero gradient', lambda f: assert_close(f([[0,0]], 0), {"norm":0.,"grads":[np.zeros(2)]})),
        ('Zero limit', lambda f: assert_close(f([[3,4]], 0)["grads"], [np.zeros(2)])),
        ('Signed gradient preserves direction', lambda f: assert_close(f([[-3,4]], 2.5)["grads"], [np.array([-1.5,2.])])),
        ('Different tensor shapes', lambda f: assert_close(f([[[3]], [4]], 2.5)["grads"], [np.array([[1.5]]),np.array([2.])])),
        ('No input mutation', lambda f: assert_close(unchanged(f, [np.array([3.,4.])], 2.5)["norm"], 5.)),
        ('Copy when below limit', lambda f: assert_close(np.shares_memory((a := np.array([3.,4.])), f([a], 10)["grads"][0]), False)),
        ('Reject empty gradient list', lambda f: rejects(f, [], 1)),
        ('Reject empty tensor', lambda f: rejects(f, [[]], 1)),
        ('Reject scalar tensor', lambda f: rejects(f, [3], 1)),
        ('Reject negative limit', lambda f: rejects(f, [[1]], -1)),
        ('Reject vector limit', lambda f: rejects(f, [[1]], [1])),
        ('Reject nonfinite gradient', lambda f: rejects(f, [[np.inf]], 1)),
        ('Reject nonfinite limit', lambda f: rejects(f, [[1]], np.nan)),
    ]
    return run_cases(namespace, 'clip_gradients', cases, mode)

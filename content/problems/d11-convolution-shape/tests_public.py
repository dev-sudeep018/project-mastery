def run_tests(namespace, mode="all"):
    cases = [
        ('Valid convolution', lambda f: assert_close(f((5,7), (3,3), (1,1), (0,0), (1,1)), (3,5))),
        ('Padding preserves shape', lambda f: assert_close(f((5,7), (3,3), (1,1), (1,1), (1,1)), (5,7))),
        ('Dilation expands the kernel', lambda f: assert_close(f((7,9), (3,3), (2,2), (0,0), (2,2)), (2,3))),
        ('Floor partial stride', lambda f: assert_close(f((6,6), (3,3), (2,2), (0,0), (1,1)), (2,2))),
        ('Different axes', lambda f: assert_close(f((4,8), (2,3), (1,2), (0,1), (1,1)), (3,4))),
        ('Reject kernel does not fit', lambda f: rejects(f, (2,2), (3,3), (1,1), (0,0), (1,1))),
        ('Reject zero dilation', lambda f: rejects(f, (4,4), (2,2), (1,1), (0,0), (0,1))),
        ('Reject negative padding', lambda f: rejects(f, (4,4), (2,2), (1,1), (-1,0), (1,1))),
        ('Reject boolean stride', lambda f: rejects(f, (4,4), (2,2), (True,1), (0,0), (1,1))),
        ('Reject missing axis', lambda f: rejects(f, (4,), (2,2), (1,1), (0,0), (1,1))),
        ("No input mutation", lambda f: assert_close(unchanged(f, (5, 7), (3, 3), (1, 1), (0, 0), (1, 1)), (3,5))),
    ]
    return run_cases(namespace, 'conv_output_shape', cases, mode)

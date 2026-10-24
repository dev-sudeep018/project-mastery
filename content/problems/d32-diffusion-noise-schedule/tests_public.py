def run_tests(namespace, mode="all"):
    cases = [
        ('Two different steps', lambda f: assert_close(f(2,.1,.2),{"betas":np.array([.1,.2]),"alpha_bar":np.array([.9,.72])})),
        ('Constant half retention', lambda f: assert_close(f(3,.5,.5),{"betas":np.full(3,.5),"alpha_bar":np.array([.5,.25,.125])})),
        ('Constant smaller noise', lambda f: assert_close(f(2,.2,.2),{"betas":np.array([.2,.2]),"alpha_bar":np.array([.8,.64])})),
        ('Include both endpoints', lambda f: assert_close(f(3,.1,.3)["betas"],np.array([.1,.2,.3]))),
        ('First entry includes noise', lambda f: assert_close(f(3,.1,.3)["alpha_bar"],np.array([.9,.72,.504]))),
        ('Long constant schedule', lambda f: assert_close(f(100,.2,.2)["alpha_bar"],.8**np.arange(1,101))),
        ('Defaults', lambda f: assert_close(f(2)["betas"],np.array([.0001,.02]))),
        ('Reject invalid step counts', lambda f: [rejects(f,value) for value in (1,10001,True,2.5,2**4096)]),
        ('Reject reversed endpoints', lambda f: rejects(f,3,.2,.1)),
        ('Reject endpoint boundaries', lambda f: [rejects(f,3,start,end) for start,end in ((0,.1),(.1,1),(-.1,.1))]),
        ('Reject nonfinite endpoints', lambda f: rejects(f,3,.1,np.inf)),
        ('Reject oversized scalar', lambda f: rejects(f,3,.1,2**4096))
    ]
    return run_cases(namespace, 'linear_noise_schedule', cases, mode)

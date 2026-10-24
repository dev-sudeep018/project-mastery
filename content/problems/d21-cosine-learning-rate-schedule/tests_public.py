def run_tests(namespace, mode="all"):
    cases = [
        ('Start of warmup', lambda f: assert_close(f(0,10,2,1),0)),
        ('End of warmup', lambda f: assert_close(f(2,10,2,1),1)),
        ('Decay midpoint', lambda f: assert_close(f(6,10,2,1,.2),.6)),
        ('Warmup halfway', lambda f: assert_close(f(1,10,2,1,.2),.5)),
        ('End is minimum', lambda f: assert_close(f(10,10,2,1,.2),.2)),
        ('After end stays minimum', lambda f: assert_close(f(20,10,2,1,.2),.2)),
        ('No warmup starts at peak', lambda f: assert_close(f(0,10,0,1,.2),1)),
        ('Reject whole-schedule warmup', lambda f: rejects(f,0,10,10,1)),
        ('Reject negative step', lambda f: rejects(f,-1,10,2,1)),
        ('Reject boolean step', lambda f: rejects(f,True,10,2,1)),
        ('Reject reversed rates', lambda f: rejects(f,1,10,2,1,2)),
        ('Reject infinite rate', lambda f: rejects(f,1,10,2,np.inf))
    ]
    return run_cases(namespace, 'cosine_lr_schedule', cases, mode)

def run_tests(namespace, mode="all"):
    cases = [
        ('Uniform predictions', lambda f: assert_close(f([[0,0]],[0],.2),np.log(2))),
        ('No smoothing', lambda f: assert_close(f([[np.log(3),0]],[0],0),np.log(4/3))),
        ('Confident correct prediction', lambda f: assert_close(f([[1000,-1000]],[0],.1),200)),
        ('Non-target-only convention', lambda f: assert_close(f([[np.log(3),0]],[0],.25),.75*np.log(4/3)+.25*np.log(4))),
        ('Three classes', lambda f: assert_close(f([[np.log(2),0,0]],[0],.2),.8*np.log(2)+.2*np.log(4))),
        ('Full smoothing', lambda f: assert_close(f([[np.log(3),0]],[0],1),np.log(4))),
        ('Batch mean', lambda f: assert_close(f([[0,0],[1000,-1000]],[0,0],.1),(np.log(2)+200)/2)),
        ('Reject single class', lambda f: rejects(f,[[1]],[0])),
        ('Reject invalid labels', lambda f: [rejects(f,[[1,2]],labels) for labels in ([2],[0.0],[True])]),
        ('Reject invalid smoothing', lambda f: [rejects(f,[[1,2]],[0],value) for value in (-.1,1.1,2**4096)]),
        ('Reject empty batch', lambda f: rejects(f,np.empty((0,2)),np.array([],dtype=int))),
        ('No mutation', lambda f: assert_close(unchanged(f,np.zeros((1,2)),np.array([0]),.2),np.log(2)))
    ]
    return run_cases(namespace, 'label_smoothed_loss', cases, mode)

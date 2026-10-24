def run_tests(namespace, mode="all"):
    cases = [
        ('Single-pixel patches', lambda f: assert_close(f([[[[1,2],[3,4]]]],1,[[2]],[1]),np.array([[[3],[5],[7],[9]]]))),
        ('Inspect a whole patch', lambda f: assert_close(f([[[[1,2],[3,4]]]],2,np.eye(4),np.zeros(4)),np.array([[[1,2,3,4]]]))),
        ('Combine channels', lambda f: assert_close(f([[[[1,2]],[[10,20]]]],1,[[1,1]],[0]),np.array([[[11],[22]]]))),
        ('Rectangular patch grid', lambda f: assert_close(f(np.arange(1,9).reshape(1,1,2,4),2,np.eye(4),np.zeros(4)),np.array([[[1,2,5,6],[3,4,7,8]]]))),
        ('Channel-first patch flattening', lambda f: assert_close(f(np.arange(1,9).reshape(1,2,2,2),2,np.eye(8),np.zeros(8)),np.arange(1,9).reshape(1,1,8))),
        ('Batch isolation', lambda f: assert_close(f(np.array([[[[2]]],[[[3]]]]),1,[[2]],[1]),np.array([[[5]],[[7]]]))),
        ('Reject partial patches', lambda f: rejects(f,np.ones((1,1,3,4)),2,np.ones((1,4)),[0])),
        ('Reject invalid patch size', lambda f: [rejects(f,np.ones((1,1,2,2)),value,np.ones((1,4)),[0]) for value in (True,0,2**4096)]),
        ('Reject weight shape', lambda f: rejects(f,np.ones((1,1,2,2)),2,np.ones((1,3)),[0])),
        ('Reject bias broadcast', lambda f: rejects(f,np.ones((1,1,1,1)),1,[[1]],[0,0])),
        ('Reject missing batch axis', lambda f: rejects(f,np.ones((1,2,2)),1,[[1]],[0])),
        ('No mutation', lambda f: assert_close(unchanged(f,np.ones((1,1,2,2)),2,np.eye(4),np.zeros(4)),np.ones((1,1,4))))
    ]
    return run_cases(namespace, 'patch_embeddings', cases, mode)

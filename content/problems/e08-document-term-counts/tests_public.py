def run_tests(namespace, mode="all"):
    cases = [
        ('Shared vocabulary with repeats', lambda f: assert_close(f([['cat','cat','dog'], ['dog','bird']]), {'vocabulary':['bird','cat','dog'],'counts':np.array([[0,2,1],[1,0,1]])})),
        ('Empty document retains its row', lambda f: assert_close(f([[], ['x']]), {'vocabulary':['x'],'counts':np.array([[0],[1]])})),
        ('Case is preserved', lambda f: assert_close(f([['a','A']]), {'vocabulary':['A','a'],'counts':np.array([[1,1]])})),
        ('All documents empty', lambda f: assert_close(f([[],[]]), {'vocabulary':[],'counts':np.zeros((2,0))})),
        ('Token order is discarded', lambda f: assert_close(f([['a','b'],['b','a']]), {'vocabulary':['a','b'],'counts':np.ones((2,2))})),
        ('Reject empty corpus', lambda f: rejects(f, [])),
        ('Reject raw text document', lambda f: rejects(f, ['text'])),
        ('Reject empty token', lambda f: rejects(f, [['']])),
        ('Reject non-string token', lambda f: rejects(f, [[1]])),
        ('Reject wrong corpus container', lambda f: rejects(f, (('x',),))),
        ("No input mutation", lambda f: assert_close(unchanged(f, [['cat','cat','dog'], ['dog','bird']]), {'vocabulary':['bird','cat','dog'],'counts':np.array([[0,2,1],[1,0,1]])})),
    ]
    return run_cases(namespace, 'document_term_counts', cases, mode)

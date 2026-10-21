def run_tests(namespace, mode="all"):
    cases = [
        ("Overlap", lambda f: assert_close(f("a b c d e",3,1), ["a b c","c d e"])),
        ("No overlap", lambda f: assert_close(f("a b c d e",2,0), ["a b","c d","e"])),
        ("Short document", lambda f: assert_close(f("one two",5,2), ["one two"])),
        ("Normalize whitespace", lambda f: assert_close(f(" a  b\nc\td ",2,0), ["a b","c d"])),
        ("Empty text", lambda f: assert_close(f("  ",3,1), [])),
        ("Maximum overlap", lambda f: assert_close(f("a b c d",3,2), ["a b c","b c d"])),
        ("Exact final window", lambda f: assert_close(f("a b c d",2,1), ["a b","b c","c d"])),
        ("Size one", lambda f: assert_close(f("a b",1,0), ["a","b"])),
        ("Zero size", lambda f: rejects(f,"a",0,0)),
        ("Excess overlap", lambda f: rejects(f,"a",2,2)),
        ("Negative overlap", lambda f: rejects(f,"a",2,-1)),
        ("Boolean size", lambda f: rejects(f,"a",True,0)),
        ("Non-string text", lambda f: rejects(f,["a"],2,0)),
    ]
    return run_cases(namespace, 'chunk_text', cases, mode)

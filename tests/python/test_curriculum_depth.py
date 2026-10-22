"""Independent properties and plausible misconceptions for the second content batch."""
import itertools
import pathlib
import unittest
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "content" / "problems"
HELPERS = (ROOT / "content" / "evaluator_helpers.py").read_text(encoding="utf-8")


def load(prefix, filename="solution.py"):
    folder, = BASE.glob(prefix + "-*")
    ns = {}
    exec((HELPERS + "\n" if filename == "tests_public.py" else "") +
         (folder / filename).read_text(encoding="utf-8"), ns)
    return ns


class CurriculumDepthTests(unittest.TestCase):
    def test_scaler_fits_training_only_and_inverts(self):
        f = load("m05")["standardize_split"]
        rng = np.random.default_rng(211)
        train, test = rng.normal(size=(20,4)), rng.normal(size=(6,4)) + 20
        a, b = f(train, test), f(train, test*100)
        np.testing.assert_array_equal(a["mean"], b["mean"])
        np.testing.assert_array_equal(a["train"], b["train"])
        np.testing.assert_allclose(a["train"].mean(axis=0), 0, atol=1e-14)
        np.testing.assert_allclose(a["train"].var(axis=0), 1)
        np.testing.assert_allclose(a["test"]*a["scale"]+a["mean"], test)

    def test_ridge_gradients_against_independent_finite_differences(self):
        f = load("m06")["ridge_gradients"]
        rng = np.random.default_rng(212)
        X, y, w = rng.normal(size=(8,3)), rng.normal(size=8), rng.normal(size=3)
        b, strength, eps = .2, .7, 1e-5
        result = f(X,y,w,b,strength)
        loss = lambda weights,bias: np.mean((X@weights+bias-y)**2)/2 + strength*np.dot(weights,weights)/2
        for i in range(len(w)):
            step = np.zeros_like(w); step[i] = eps
            self.assertAlmostEqual(result["dw"][i], (loss(w+step,b)-loss(w-step,b))/(2*eps), places=7)
        self.assertAlmostEqual(result["db"], (loss(w,b+eps)-loss(w,b-eps))/(2*eps), places=7)
        duplicated = f(np.tile(X,(2,1)), np.tile(y,2), w,b,strength)
        np.testing.assert_allclose(duplicated["dw"], result["dw"])
        self.assertAlmostEqual(duplicated["loss"], result["loss"])

    def test_relu_chain_rule_away_from_boundary(self):
        f = load("d05")["relu_backward"]
        x, upstream, eps = np.array([[-2.,3.],[.5,-.4]]), np.array([[4.,-2.],[3.,1.]]), 1e-6
        result = f(x,upstream)
        loss = lambda a: float(np.sum(np.maximum(a,0)*upstream))
        for index in np.ndindex(x.shape):
            step = np.zeros_like(x); step[index] = eps
            self.assertAlmostEqual(result["dx"][index], (loss(x+step)-loss(x-step))/(2*eps), places=7)

    def test_dropout_expectation_over_all_masks_and_clip_direction(self):
        dropout, clip = load("d06")["inverted_dropout"], load("d07")["clip_gradients"]
        x = np.array([2.,-4.,6.])
        # All eight masks are equally likely for p=0.5; no statistical/flaky tolerance.
        outputs = [dropout(x,np.array(mask),.5,True) for mask in itertools.product([False,True],repeat=3)]
        np.testing.assert_allclose(np.mean(outputs,axis=0), x)
        rng = np.random.default_rng(213)
        for limit in [0., .1, 2., 100.]:
            grads = [rng.normal(size=(3,2)), rng.normal(size=4)]
            before = np.concatenate([g.ravel() for g in grads])
            result = clip(grads,limit)
            after = np.concatenate([g.ravel() for g in result["grads"]])
            self.assertLessEqual(np.linalg.norm(after), limit+1e-12)
            self.assertAlmostEqual(result["norm"], np.linalg.norm(before))
            np.testing.assert_allclose(after, before*min(1,limit/np.linalg.norm(before)))

    def test_retrieval_representation_and_metric_invariants(self):
        tfidf, ndcg = load("e05")["tfidf_weights"], load("e07")["ndcg_at_k"]
        counts = np.array([[2,1,0],[1,3,1],[0,0,0]])
        a = tfidf(counts)
        scaled = counts.copy(); scaled[0] *= 3
        np.testing.assert_allclose(a["weights"],tfidf(scaled)["weights"])
        np.testing.assert_allclose(np.linalg.norm(a["weights"],axis=1), [1,1,0])
        judgments = {"a":3,"b":2,"c":1}
        for ranking in itertools.permutations(judgments):
            value = ndcg(list(ranking),judgments,3)
            self.assertGreaterEqual(value,0)
            self.assertLessEqual(value,1)
        self.assertEqual(ndcg(["a","b","c"],judgments,3),1)

    def test_evaluators_reject_conceptual_mistakes_on_valid_inputs(self):
        def leaking(train,test):
            result = load("m05")["standardize_split"](np.vstack([train,test]),test)
            result["train"] = result["train"][:len(train)]
            return result

        def penalized_bias(X,y,w,b,strength):
            r = load("m06")["ridge_gradients"](X,y,w,b,strength)
            r["loss"] += strength*b*b/2; r["db"] += strength*b
            return r

        def strict_threshold(y,scores,threshold):
            # Adjacent representable threshold changes >= into > for finite ties.
            return load("m07")["binary_metrics"](y,scores,np.nextafter(threshold,np.inf))

        def clip_upstream(x,upstream):
            return {"output":np.maximum(x,0),"dx":np.maximum(upstream,0)}

        def unscaled_dropout(x,keep,p,training):
            return np.asarray(x)*keep if training else np.asarray(x).copy()

        def per_coordinate(grads,limit):
            r = load("d07")["clip_gradients"](grads,limit)
            r["grads"] = [np.clip(g,-limit,limit) for g in grads]
            return r

        def occurrence_idf(counts):
            r = load("e05")["tfidf_weights"](counts)
            r["idf"] = np.log((1+len(counts))/(1+np.asarray(counts).sum(axis=0)))+1
            return r

        def relevance_only(relevance,similarity,k,weight):
            return sorted(range(len(relevance)),key=lambda i:(-relevance[i],i))[:k]

        def oracle_ranking(ranked,relevance,k):
            return load("e07")["ndcg_at_k"](sorted(set(ranked),key=lambda d:-relevance.get(d,0)),relevance,k)

        mutants = [("m05","standardize_split",leaking), ("m06","ridge_gradients",penalized_bias),
            ("m07","binary_metrics",strict_threshold), ("d05","relu_backward",clip_upstream),
            ("d06","inverted_dropout",unscaled_dropout), ("d07","clip_gradients",per_coordinate),
            ("e05","tfidf_weights",occurrence_idf), ("e06","mmr_select",relevance_only),
            ("e07","ndcg_at_k",oracle_ranking)]
        for prefix,name,fn in mutants:
            with self.subTest(problem=prefix), np.errstate(all="ignore"):
                results = load(prefix,"tests_public.py")["run_tests"]({name:fn})
                self.assertTrue(any(not r["passed"] for r in results if not r["name"].startswith(("Reject", "Validate"))), results)

    def test_boolean_assertions_do_not_accept_numeric_substitutes(self):
        ns = {}; exec(HELPERS,ns)
        check = ns["assert_close"]
        check(True,True); check(np.bool_(False),False)
        for actual,expected in [(1,True),(False,0),(True,False)]:
            with self.subTest(actual=actual,expected=expected), self.assertRaises(AssertionError):
                check(actual,expected)

"""Independent properties and misconception checks for the 30-activity batch."""
import json
import pathlib
import unittest

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "content/problems"
HELPERS = (ROOT / "content/evaluator_helpers.py").read_text(encoding="utf-8")


def load(prefix, filename="solution.py"):
    folder, = BASE.glob(prefix + "-*")
    namespace = {}
    exec((HELPERS + "\n" if filename == "tests_public.py" else "") +
         (folder / filename).read_text(encoding="utf-8"), namespace)
    return namespace


def function(prefix):
    ns = load(prefix)
    return next(value for name,value in ns.items() if not name.startswith("_") and callable(value))


class CurriculumBatch03Tests(unittest.TestCase):
    def test_weighted_moments_and_covariance_invariants(self):
        rng = np.random.default_rng(301)
        x, weights = rng.normal(size=20), rng.uniform(.1,2,size=20)
        moments = function("m08")
        original = moments(x,weights)
        self.assertAlmostEqual(original["mean"], np.average(x,weights=weights))
        scaled = moments(x,weights*11)
        self.assertAlmostEqual(original["variance"], scaled["variance"])
        shifted = moments(x+7,weights)
        self.assertAlmostEqual(original["variance"], shifted["variance"])
        self.assertAlmostEqual(original["mean"]+7, shifted["mean"])
        X = rng.normal(size=(25,4))
        covariance = function("m09")(X)
        np.testing.assert_allclose(covariance,np.cov(X,rowvar=False))
        np.testing.assert_allclose(covariance,function("m09")(X+[1,3,7,-2]))
        self.assertGreaterEqual(np.linalg.eigvalsh(covariance).min(),-1e-12)

    def test_geometry_and_projection_residuals(self):
        rng = np.random.default_rng(302)
        X, Y = rng.normal(size=(8,4)), rng.normal(size=(5,4))
        distances = function("m12")
        np.testing.assert_allclose(distances(X,Y),distances(Y,X).T)
        np.testing.assert_allclose(np.diag(distances(X,X)),0)
        np.testing.assert_allclose(distances(X+[1,2,3,4],Y+[1,2,3,4]),distances(X,Y))
        basis, _ = np.linalg.qr(rng.normal(size=(4,4)))
        mean = rng.normal(size=4)
        project = function("m15")
        result = project(X,mean,basis[:2])
        residual = X-result["reconstruction"]
        np.testing.assert_allclose(residual @ basis[:2].T,0,atol=1e-12)
        np.testing.assert_allclose(project(X,mean,basis)["reconstruction"],X,atol=1e-12)
        centers = Y[:2]
        before = function("m14")(X,centers)["inertia"]
        after = function("m14")(X,np.vstack([centers,X[0]]))["inertia"]
        self.assertLessEqual(after,before+1e-12)

    def test_split_indices_are_disjoint_complete_and_stratified(self):
        labels = np.array([4,9,4,7,9,7,4,7,9,4,4,9])
        for fraction in [.01,.25,.5,.9,.99]:
            split = function("m17")(labels,fraction)
            train,test = split["train"],split["test"]
            self.assertFalse(set(train) & set(test))
            self.assertEqual(sorted(train+test),list(range(len(labels))))
            self.assertEqual(set(labels[train]),set(labels))
            self.assertEqual(set(labels[test]),set(labels))

    def test_sigmoid_stability_and_embedding_chain_rule(self):
        sigmoid = function("d08")
        with np.errstate(over="raise",invalid="raise"):
            result = sigmoid(np.array([-1000.,0.,1000.]))
        np.testing.assert_allclose(result["output"],[0,.5,1])
        x, eps = np.array([-2.,-.5,.5,2.]), 1e-6
        difference = (sigmoid(x+eps)["output"]-sigmoid(x-eps)["output"])/(2*eps)
        np.testing.assert_allclose(sigmoid(x)["derivative"],difference,atol=1e-9)
        lookup, backward = function("d12"),function("d13")
        table = np.arange(12,dtype=float).reshape(4,3)/10
        ids = np.array([2,0,2,1])
        upstream = np.array([[1,2,3],[-2,0,1],[3,-1,2],[.5,2,-3]])
        gradient = backward(ids,upstream,4)
        loss = lambda t: float(np.sum(lookup(t,ids)*upstream))
        for index in np.ndindex(table.shape):
            step = np.zeros_like(table); step[index] = eps
            self.assertAlmostEqual(gradient[index],(loss(table+step)-loss(table-step))/(2*eps),places=7)
        output = lookup(table,[0,1]); output[0,0] = 100
        self.assertEqual(table[0,0],0)

    def test_adam_constant_gradient_trajectory(self):
        adam = function("d15")
        parameters = np.array([1.,-2.,3.])
        gradient = np.array([2.,-4.,0.])
        m, v = np.zeros(3),np.zeros(3)
        for t in range(1,7):
            previous = parameters.copy()
            result = adam(parameters,gradient,m,v,t,.1,.9,.99,.001)
            parameters,m,v = result["parameters"],result["m"],result["v"]
            np.testing.assert_allclose(m/(1-.9**t),gradient)
            np.testing.assert_allclose(v/(1-.99**t),gradient**2)
            np.testing.assert_allclose(parameters,previous-.1*gradient/(np.abs(gradient)+.001))

    def test_position_pairs_and_mask_contract(self):
        pe = function("d16")(13,8)
        np.testing.assert_allclose(pe[:,0::2]**2+pe[:,1::2]**2,1,atol=1e-12)
        lengths = [0,1,3,5]
        mask = function("d17")(lengths,5)
        self.assertEqual(mask.dtype,np.dtype(bool))
        for batch,length in enumerate(lengths):
            for query in range(5):
                for key in range(5):
                    self.assertEqual(mask[batch,query,key],query < length and key < length and key <= query)
        padded = function("e10")([[0,2],[],[3]],0)
        np.testing.assert_array_equal(padded["mask"].sum(axis=1),[2,0,1])
        ns = {}; exec(HELPERS,ns)
        with self.assertRaises(AssertionError):
            ns["assert_close"](mask.astype(int),mask)

    def test_text_representations_and_selection_properties(self):
        documents = [["x","y","x"],[],["y","z"]]
        counts = function("e08")(documents)
        np.testing.assert_array_equal(counts["counts"].sum(axis=1),list(map(len,documents)))
        merged = function("e12")(["a","b","a","a","b"],("a","b"))
        self.assertEqual("".join(merged),"abaab")
        self.assertEqual(merged,["ab","a","ab"])
        bm25 = function("e09")
        original = bm25(counts["counts"],[1,2,0],1.2,.75)
        np.testing.assert_allclose(bm25(counts["counts"],[3,6,0],1.2,.75),3*original)
        rng = np.random.default_rng(303)
        costs = rng.integers(1,20,size=20)
        scores = rng.random(20)
        for budget in [0,1,10,30,100]:
            chosen = function("e13")(costs,scores,budget)
            self.assertEqual(len(chosen),len(set(chosen)))
            self.assertLessEqual(costs[chosen].sum(),budget)
            self.assertEqual(chosen,sorted(chosen,key=lambda i:(-scores[i],i)))

    def test_probability_metrics_invariants(self):
        rng = np.random.default_rng(304)
        labels = np.array([0,1]*12)
        probabilities = rng.uniform(.01,.99,size=len(labels))
        auc,brier,calibrate = function("e15"),function("e16"),function("e17")
        self.assertAlmostEqual(auc(labels,probabilities),auc(labels,3*probabilities-5))
        self.assertAlmostEqual(auc(labels,probabilities)+auc(labels,-probabilities),1)
        self.assertAlmostEqual(brier(labels,probabilities),brier(1-labels,1-probabilities))
        for bins in [1,2,5,40]:
            result = calibrate(labels,probabilities,bins)
            self.assertEqual(result["counts"].sum(),len(labels))
            self.assertAlmostEqual(result["counts"] @ result["mean_probability"],probabilities.sum())
            self.assertAlmostEqual(result["counts"] @ result["positive_fraction"],labels.sum())
            self.assertGreaterEqual(result["ece"],0)
            self.assertLessEqual(result["ece"],1)

    def test_every_evaluator_catches_a_conceptual_mistake_on_valid_input(self):
        refs = {prefix:function(prefix) for prefix in [f"{domain}{i:02}" for domain in "mde" for i in range(8,18)]}

        def wrong_inertia(X,centers):
            result = refs["m14"](X,centers)
            result["inertia"] /= len(X)
            return result

        def no_priors(X,priors,means,variances):
            result = refs["m16"](X,priors,means,variances)
            result["log_joint"] -= np.log(priors)
            result["predictions"] = np.argmax(result["log_joint"],axis=1)
            return result

        def global_split(labels,fraction):
            count = int(len(labels)*fraction)
            return {"train":list(range(count)),"test":list(range(count,len(labels)))}

        def sigmoid_wrong_derivative(x):
            result = refs["d08"](x)
            result["derivative"] = result["output"]
            return result

        def overwrite_gradient(ids,upstream,size):
            result = np.zeros((size,np.asarray(upstream).shape[1]))
            for token,row in zip(ids,upstream):
                result[token] = row
            return result

        def adam_without_correction(parameters,gradient,m,v,t,rate,b1,b2,eps):
            result = refs["d15"](parameters,gradient,m,v,t,rate,b1,b2,eps)
            result["parameters"] = np.asarray(parameters)-rate*result["m"]/(np.sqrt(result["v"])+eps)
            return result

        def one_frequency(length,dimensions):
            return np.tile(refs["d16"](length,2),(1,dimensions//2))

        def mask_keys_only(lengths,size):
            return np.tri(size,dtype=bool)[None,:,:] & (np.arange(size)[None,None,:] < np.asarray(lengths)[:,None,None])

        def binary_counts(documents):
            result = refs["e08"](documents)
            result["counts"] = (result["counts"] > 0).astype(int)
            return result

        def mask_by_value(sequences,pad):
            result = refs["e10"](sequences,pad)
            result["mask"] = result["tokens"] != pad
            return result

        def overlapping_merge(tokens,pair):
            output = []
            for i,token in enumerate(tokens):
                if i+1 < len(tokens) and (token,tokens[i+1]) == tuple(pair):
                    output.append(token+tokens[i+1])
                elif i == 0 or (tokens[i-1],token) != tuple(pair):
                    output.append(token)
            return output

        def stop_at_oversized(costs,scores,budget):
            selected = []
            for i in sorted(range(len(costs)),key=lambda i:(-scores[i],i)):
                if costs[i] > budget:
                    break
                selected.append(i); budget -= costs[i]
            return selected

        def no_tie_credit(labels,scores):
            labels,scores = np.asarray(labels),np.asarray(scores)
            return float(np.mean(scores[labels==1][:,None] > scores[labels==0][None,:]))

        def unweighted_calibration(labels,probabilities,bins):
            result = refs["e17"](labels,probabilities,bins)
            used = result["counts"] > 0
            result["ece"] = float(np.abs(result["mean_probability"]-result["positive_fraction"])[used].mean())
            return result

        mutants = {
            "m08":lambda x,w:refs["m08"](x,np.ones(len(x))),
            "m09":lambda X:refs["m09"](X)*(len(X)-1)/len(X),
            "m10":lambda x,d:refs["m10"](x,d)[:,::-1],
            "m11":lambda labels,n:refs["m11"](labels,int(max(labels))+1),
            "m12":lambda X,Y:np.sqrt(refs["m12"](X,Y)),
            "m13":lambda X,y,Q,k:refs["m13"](X,y,Q,1),
            "m14":wrong_inertia,
            "m15":lambda X,mean,C:refs["m15"](X,np.asarray(X).mean(axis=0),C),
            "m16":no_priors,
            "m17":global_split,
            "d08":sigmoid_wrong_derivative,
            "d09":lambda X,K:refs["d09"](X,np.asarray(K)[::-1,::-1]),
            "d10":lambda X,window,stride:np.maximum(refs["d10"](X,window,stride),0),
            "d11":lambda shape,kernel,stride,padding,dilation:refs["d11"](shape,kernel,stride,padding,(1,1)),
            "d12":lambda table,ids:refs["d12"](table,sorted(set(ids))),
            "d13":overwrite_gradient,
            "d14":lambda p,g,v,rate,b:refs["d14"](p,np.asarray(g)*(1-b),v,rate,b),
            "d15":adam_without_correction,
            "d16":one_frequency,
            "d17":mask_keys_only,
            "e08":binary_counts,
            "e09":lambda counts,query,k1,b:refs["e09"](counts,query,k1,0),
            "e10":mask_by_value,
            "e11":lambda words,freq:refs["e11"](words,[1]*len(words)),
            "e12":overlapping_merge,
            "e13":stop_at_oversized,
            "e14":lambda actual,predicted,n:refs["e14"](actual,predicted,n).T,
            "e15":no_tie_credit,
            "e16":lambda labels,probabilities:np.sqrt(refs["e16"](labels,probabilities)),
            "e17":unweighted_calibration,
        }
        self.assertEqual(len(mutants),30)
        for prefix,mutant in mutants.items():
            with self.subTest(problem=prefix), np.errstate(all="ignore"):
                results = load(prefix,"tests_public.py")["run_tests"]({refs[prefix].__name__:mutant})
                # Require an incorrect result on a valid case, not just missing validation.
                failed = [r for r in results if not r["passed"] and not r["name"].startswith(("Reject","No input mutation"))]
                self.assertTrue(failed,results)
                self.assertTrue(any(r["message"].startswith("AssertionError") for r in failed),failed)

    def test_adaptation_provenance_is_preserved_in_distributed_reference(self):
        provenance = json.loads((ROOT/"content/batch-03-provenance.json").read_text(encoding="utf-8"))
        expected = {f"{domain}{i:02}" for domain in "mde" for i in range(8,18)}
        self.assertEqual({item["id"] for item in provenance["items"]},expected)
        self.assertEqual(len(provenance["items"]),30)
        adaptations = [item for item in provenance["items"] if item["origin"] == "code-adaptation"]
        self.assertEqual(len(adaptations),1)
        adaptation = adaptations[0]
        notice = (ROOT/adaptation["notice"]).read_text(encoding="utf-8")
        reference = (BASE/"d09-image-cross-correlation/solution.py").read_text(encoding="utf-8")
        for text in (notice,reference):
            self.assertIn(adaptation["upstream_revision"],text)
            self.assertIn("Copyright 2019 Amazon.com",text)
            self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"',text)
            self.assertIn("MIT-0",text)

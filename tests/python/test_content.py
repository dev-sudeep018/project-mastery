import pathlib
import json
import os
import unittest
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROBLEMS = ROOT / "content" / "problems"
HELPERS = (ROOT / "content" / "evaluator_helpers.py").read_text(encoding="utf-8")


class ContentTests(unittest.TestCase):
    def test_every_reference_passes(self):
        folders = sorted(folder for folder in PROBLEMS.iterdir() if folder.is_dir())
        selection = os.environ.get("MASTERY_CONTENT_FOLDERS")
        if selection is not None:
            names = json.loads(selection)
            self.assertIsInstance(names, list)
            self.assertTrue(names, "A batch must select at least one package")
            known = {folder.name for folder in folders}
            self.assertTrue(all(name in known for name in names), "Unknown package in batch")
            folders = [folder for folder in folders if folder.name in names]
        for folder in folders:
            with self.subTest(problem=folder.name):
                evaluator, reference = {}, {}
                exec(HELPERS + "\n" + (folder / "tests_public.py").read_text(encoding="utf-8"), evaluator)
                exec((folder / "solution.py").read_text(), reference)
                results = evaluator["run_tests"](reference)
                self.assertGreaterEqual(len(results), 10)
                self.assertEqual(len(results), json.loads((folder / "lesson.json").read_text(encoding="utf-8"))["test_count"])
                self.assertTrue(all(r["passed"] for r in results), results)
                starter = {}
                exec((folder / "starter.py").read_text(encoding="utf-8"), starter)
                self.assertTrue(any(not r["passed"] for r in evaluator["run_tests"](starter)))
                self.assertEqual(len(evaluator["run_tests"](reference, "sample")), 3)
                entrypoint = next(name for name in starter if callable(starter[name]) and not name.startswith("_"))
                self.assertTrue(any(not r["passed"] for r in evaluator["run_tests"]({entrypoint:lambda *a,**k: 0})))

    def test_linear_gradients_against_finite_differences(self):
        namespace = {}
        exec((PROBLEMS / "m03-linear-regression-gradients" / "solution.py").read_text(), namespace)
        rng = np.random.default_rng(803)
        X, y, w, b = rng.normal(size=(7,3)), rng.normal(size=7), rng.normal(size=3), .4
        result = namespace["linear_gradients"](X,y,w,b)
        loss = lambda weights,bias: np.mean((X @ weights + bias-y)**2)/2
        for i in range(3):
            step = np.zeros(3); step[i]=1e-5
            self.assertAlmostEqual(result["dw"][i], (loss(w+step,b)-loss(w-step,b))/2e-5, places=7)
        self.assertAlmostEqual(result["db"], (loss(w,b+1e-5)-loss(w,b-1e-5))/2e-5, places=7)

    def test_attention_mask_and_row_invariants(self):
        namespace = {}
        exec((PROBLEMS / "d04-masked-attention" / "solution.py").read_text(), namespace)
        rng=np.random.default_rng(42)
        Q,K,V=rng.normal(size=(5,4)),rng.normal(size=(7,4)),rng.normal(size=(7,3))
        mask=rng.random((5,7))>.4;mask[0]=False
        result=namespace["masked_attention"](Q,K,V,mask)
        np.testing.assert_allclose(result["weights"].sum(axis=1), mask.any(axis=1).astype(float))
        np.testing.assert_array_equal(result["weights"][~mask],0)
        np.testing.assert_allclose(result["output"],result["weights"] @ V)

    def test_evaluator_rejects_incorrect_solutions(self):
        folder = PROBLEMS / "m02-stable-softmax"
        evaluator = {}
        exec((folder / "tests_public.py").read_text(), evaluator)
        wrong = [
            lambda x: np.exp(x) / np.sum(np.exp(x)),
            lambda x: np.ones_like(x) / np.size(x),
            lambda x: np.asarray(x) / np.sum(x),
            lambda x: np.array([0.09003057, 0.24472847, 0.66524096]),
        ]
        for fn in wrong:
            with self.subTest(solution=fn), np.errstate(all="ignore"):
                self.assertTrue(any(not r["passed"] for r in evaluator["run_tests"]({"softmax": fn})))

    def test_reference_shift_invariance_and_input_integrity(self):
        namespace = {}
        exec((PROBLEMS / "m02-stable-softmax" / "solution.py").read_text(), namespace)
        rng = np.random.default_rng(721)
        for size in [1, 3, 17, 512]:
            x = rng.normal(size=size)
            before = x.copy()
            baseline = namespace["softmax"](x)
            np.testing.assert_array_equal(x, before)
            for shift in [-10000, 0, 10000]:
                np.testing.assert_allclose(namespace["softmax"](x + shift), baseline, atol=1e-7, rtol=1e-6)


if __name__ == "__main__":
    unittest.main()

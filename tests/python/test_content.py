import pathlib
import unittest
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROBLEMS = ROOT / "content" / "problems"


class ContentTests(unittest.TestCase):
    def test_every_reference_passes(self):
        for folder in PROBLEMS.iterdir():
            if not folder.is_dir():
                continue
            with self.subTest(problem=folder.name):
                evaluator, reference = {}, {}
                exec((folder / "tests_public.py").read_text(), evaluator)
                exec((folder / "solution.py").read_text(), reference)
                results = evaluator["run_tests"](reference)
                self.assertGreaterEqual(len(results), 10)
                self.assertTrue(all(r["passed"] for r in results), results)

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

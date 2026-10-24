"""Independent invariants and plausible misconceptions for licensed adaptations."""
import json
import pathlib
import unittest

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / 'content/problems'
HELPERS = (ROOT / 'content/evaluator_helpers.py').read_text(encoding='utf-8')


def load(prefix, name='solution.py'):
    folder, = BASE.glob(prefix + '-*')
    namespace = {}
    exec((HELPERS + '\n' if name == 'tests_public.py' else '') +
         (folder/name).read_text(encoding='utf-8'), namespace)
    return namespace


class PlatformPilotTests(unittest.TestCase):
    def test_rms_scale_and_sign_without_centering(self):
        f = load('d18')['rms_norm']
        rng = np.random.default_rng(418)
        x = rng.normal(size=(3,5,8)) + 4
        y = f(x, np.ones(8), 1e-6)
        expected_energy = np.sum(x*x, axis=-1) / (np.mean(x*x, axis=-1) + 1e-6)
        np.testing.assert_allclose(np.sum(y*y, axis=-1), expected_energy)
        np.testing.assert_allclose(f(-x,np.ones(8)), -y)
        self.assertGreater(y.mean(), .9)

    def test_rope_preserves_norms_and_common_shift_dot_products(self):
        f = load('d19')['apply_rope']
        rng = np.random.default_rng(419)
        q,k = rng.normal(size=(2,6,8)),rng.normal(size=(2,6,8))
        qr,kr = f(q,k)
        np.testing.assert_allclose(np.linalg.norm(qr,axis=-1),np.linalg.norm(q,axis=-1))
        np.testing.assert_allclose(np.linalg.norm(kr,axis=-1),np.linalg.norm(k,axis=-1))
        qshift,kshift = f(np.pad(q,((0,0),(3,0),(0,0))), np.pad(k,((0,0),(3,0),(0,0))))
        np.testing.assert_allclose(qr[:,1] @ kr[:,4].T, qshift[:,4] @ kshift[:,7].T, atol=1e-12)
        np.testing.assert_allclose(qr[:,0],q[:,0])

    def test_lora_matches_merged_weight_and_rank_parameterization(self):
        f = load('d20')['lora_linear']
        rng = np.random.default_rng(420)
        x,w,bias,a,b = rng.normal(size=(3,4)),rng.normal(size=(5,4)),rng.normal(size=5),rng.normal(size=(2,4)),rng.normal(size=(5,2))
        np.testing.assert_allclose(f(x,w,bias,a,b,3), x @ (w+1.5*b@a).T+bias)
        np.testing.assert_allclose(f(x,w,bias,a*7,b/7,3),f(x,w,bias,a,b,3))
        np.testing.assert_allclose(f(x,w,bias,a,b*0,3),x@w.T+bias)

    def test_quantization_error_and_channel_scaling(self):
        f = load('e18')['quantized_linear']
        rng = np.random.default_rng(421)
        x,w = rng.normal(size=(4,6)),rng.normal(size=(5,6))
        result=f(x,w,np.zeros(5))
        reconstructed=result['weight_int8'].astype(float)*result['scale']
        self.assertEqual(result['weight_int8'].dtype,np.int8)
        self.assertTrue(np.all(np.abs(w-reconstructed) <= result['scale']/2+1e-12))
        multipliers=np.array([1,2,4,8,16])[:,None]
        scaled=f(x,w*multipliers,np.zeros(5))
        np.testing.assert_array_equal(scaled['weight_int8'],result['weight_int8'])
        np.testing.assert_allclose(scaled['output'],result['output']*multipliers.T)
        np.testing.assert_allclose(result['output'],x@reconstructed.T)

    def test_schedule_monotonic_phases_and_endpoints(self):
        f=load('d21')['cosine_lr_schedule']
        values=np.array([f(step,100,10,.01,.001) for step in range(121)])
        self.assertTrue(np.all(np.diff(values[:11])>0))
        self.assertTrue(np.all(np.diff(values[10:101])<0))
        np.testing.assert_array_equal(values[100:],np.full(21,.001))
        self.assertAlmostEqual(values[55],.0055)
        self.assertAlmostEqual(f(0,100,0,.01,.001),.01)

    def test_focal_shift_invariance_and_uncapped_wrong_predictions(self):
        f=load('d22')['focal_loss']
        rng=np.random.default_rng(422)
        logits=rng.normal(size=(6,4)); labels=np.array([0,1,2,3,0,1])
        self.assertAlmostEqual(f(logits,labels),f(logits+10000,labels),places=10)
        expected=np.mean(np.log(np.exp(logits).sum(axis=1))-logits[np.arange(6),labels])
        self.assertAlmostEqual(f(logits,labels,1,0),expected)
        self.assertLessEqual(f(logits,labels,1,5),f(logits,labels,1,2))
        self.assertEqual(f([[1000,-1000]],[1],1,2),2000)

    def test_public_checks_reject_valid_input_misconceptions(self):
        mistakes = {
            'd18': ('rms_norm',lambda x,w,eps=1e-6: (np.asarray(x)-np.mean(x,axis=-1,keepdims=True))/np.sqrt(np.var(x,axis=-1,keepdims=True)+eps)*w),
            'd19': ('apply_rope',lambda q,k: (np.asarray(q),np.asarray(k))),
            'd20': ('lora_linear',lambda x,w,bias,a,b,alpha=1: np.asarray(x)@np.asarray(w).T+bias+(np.asarray(x)@np.asarray(a).T@np.asarray(b).T)*alpha),
            'e18': ('quantized_linear',lambda x,w,bias: {'weight_int8':np.asarray(w),'scale':np.ones((len(w),1)), 'output':np.asarray(x)@np.asarray(w).T+bias}),
            'd21': ('cosine_lr_schedule',lambda step,total,warmup,peak,floor=0: floor+(peak-floor)*max(0,1-step/total)),
            'd22': ('focal_loss',lambda logits,targets,alpha=.25,gamma=2: load('d22')['focal_loss'](logits,targets,alpha,0)),
        }
        for prefix,(entrypoint,wrong) in mistakes.items():
            with self.subTest(activity=prefix):
                results=load(prefix,'tests_public.py')['run_tests']({entrypoint:wrong})
                self.assertTrue(any(not row['passed'] and row['message'].startswith('AssertionError:') and not row['name'].startswith('Reject') for row in results),results)

    def test_oversized_integer_scalars_raise_documented_value_error(self):
        oversized = 2 ** 4096
        calls = [
            ('d18', 'rms_norm', ([1], [1], oversized)),
            ('d20', 'lora_linear', ([1], [[1]], [0], [[1]], [[1]], oversized)),
            ('d21', 'cosine_lr_schedule', (1, 10, 2, oversized)),
            ('d21', 'cosine_lr_schedule', (1, 10, 2, 1, oversized)),
            ('d21', 'cosine_lr_schedule', (oversized, 10, 2, 1)),
            ('d22', 'focal_loss', ([[1, 2]], [0], oversized, 2)),
            ('d22', 'focal_loss', ([[1, 2]], [0], 1, oversized)),
        ]
        for prefix, name, args in calls:
            with self.subTest(activity=prefix, function=name):
                with self.assertRaises(ValueError):
                    load(prefix)[name](*args)

    def test_upstream_notices_survive_reference_packaging(self):
        manifest=json.loads((ROOT/'content/platform-pilot-provenance.json').read_text())
        self.assertEqual(len(manifest['items']),6)
        for item in manifest['items']:
            folder=BASE/item['folder']
            source=(folder/'solution.py').read_text(encoding='utf-8')
            notice=(ROOT/item['notice']).read_text(encoding='utf-8')
            for text in ['Copyright (c) 2024 duoan','Copyright (c) 2024 kiren','Permission is hereby granted','THE SOFTWARE IS PROVIDED',item['upstream_url']]:
                self.assertIn(text,source)
                self.assertIn(text,notice)
            self.assertEqual(len(item['upstream_sha256']),64)


if __name__ == '__main__':
    unittest.main()

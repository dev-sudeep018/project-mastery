"""Numerical properties and conceptual counterexamples for the second platform batch."""
import json
import math
import pathlib
import unittest

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / 'content/problems'
HELPERS = (ROOT / 'content/evaluator_helpers.py').read_text(encoding='utf-8')


def load(prefix, filename='solution.py'):
    folder, = BASE.glob(prefix+'-*')
    namespace = {}
    source = (HELPERS+'\n' if filename == 'tests_public.py' else '')
    exec(source+(folder/filename).read_text(encoding='utf-8'), namespace)
    return namespace


class PlatformBatch02Tests(unittest.TestCase):
    def test_gelu_symmetry_and_local_derivative(self):
        f = load('d23')['gelu']
        x = np.linspace(-4,4,101)
        np.testing.assert_allclose(f(x)-f(-x),x,atol=1e-14)
        numerical = (f(x+1e-5)-f(x-1e-5))/2e-5
        expected = np.array([.5*(1+math.erf(v/math.sqrt(2)))+v*math.exp(-v*v/2)/math.sqrt(2*math.pi) for v in x])
        np.testing.assert_allclose(numerical,expected,atol=1e-9,rtol=1e-7)
        self.assertLess(f(np.array([-1.]))[0],0)

    def test_swiglu_matches_scalar_branch_composition(self):
        f = load('d24')['swiglu']
        rng = np.random.default_rng(524)
        x, wv, wg, wo = rng.normal(size=(2,3)),rng.normal(size=(3,4)),rng.normal(size=(3,4)),rng.normal(size=(4,2))
        expected = np.zeros((2,2))
        for i in range(2):
            for h in range(4):
                value = sum(x[i,j]*wv[j,h] for j in range(3))
                gate = sum(x[i,j]*wg[j,h] for j in range(3))
                for o in range(2):
                    expected[i,o] += value*gate/(1+math.exp(-gate))*wo[h,o]
        np.testing.assert_allclose(f(x,wv,wg,wo),expected)
        np.testing.assert_allclose(f(x,wv*2,wg,wo/2),expected)
        np.testing.assert_array_equal(f(x,wv,wg*0,wo),np.zeros((2,2)))

    def test_batch_normalization_state_and_inference_independence(self):
        f = load('d25')['batch_norm']
        first = f([[1],[3]],[1],[0],[0],[0],True,.5,3)
        second = f([[5],[7]],[1],[0],first['running_mean'],first['running_var'],True,.5,3)
        np.testing.assert_allclose(second['running_mean'],[3.5])
        np.testing.assert_allclose(second['running_var'],[.75])
        np.testing.assert_allclose(second['output'],[[-.5],[.5]])
        alone = f([[9]],[2],[1],second['running_mean'],second['running_var'],False)['output']
        together = f([[9],[-1000]],[2],[1],second['running_mean'],second['running_var'],False)['output']
        np.testing.assert_array_equal(alone,together[:1])
        rng = np.random.default_rng(525)
        out = f(rng.normal(size=(9,4)),np.ones(4),np.zeros(4),np.zeros(4),np.ones(4))['output']
        np.testing.assert_allclose(out.mean(axis=0),0,atol=1e-14)

    def test_label_smoothing_is_linear_in_target_mass(self):
        f = load('d26')['label_smoothed_loss']
        rng = np.random.default_rng(526)
        x, labels = rng.normal(size=(8,4)),np.arange(8)%4
        base, other = f(x,labels,0),f(x,labels,1)
        self.assertAlmostEqual(f(x,labels,.3),.7*base+.3*other)
        self.assertAlmostEqual(f(x+np.arange(8)[:,None]*1000,labels,.3),f(x,labels,.3),places=10)
        # Relabeling class columns and target IDs together preserves the objective.
        perm = np.array([2,0,3,1])
        inverse = np.argsort(perm)
        self.assertAlmostEqual(f(x[:,perm],inverse[labels],.3),f(x,labels,.3))

    def test_contrastive_geometry_and_temperature_direction(self):
        f = load('d27')['contrastive_loss']
        rng = np.random.default_rng(527)
        q,k = rng.normal(size=(7,5)),rng.normal(size=(7,5))
        q /= np.linalg.norm(q,axis=1,keepdims=True)
        k /= np.linalg.norm(k,axis=1,keepdims=True)
        rotation,_ = np.linalg.qr(rng.normal(size=(5,5)))
        self.assertAlmostEqual(f(q,k),f(q@rotation,k@rotation))
        perm = rng.permutation(7)
        self.assertAlmostEqual(f(q,k),f(q[perm],k[perm]))
        self.assertLess(f(np.eye(2),np.eye(2),.1),f(np.eye(2),np.eye(2),1))
        self.assertGreater(f(np.eye(2),np.eye(2)[::-1],.1),f(np.eye(2),np.eye(2)[::-1],1))
        self.assertAlmostEqual(f(np.tile([1.,0.],(5,1)),np.tile([1.,0.],(5,1))),math.log(5))

    def test_graph_layers_follow_node_permutations(self):
        rng = np.random.default_rng(528)
        graph = rng.integers(0,2,size=(6,6)); graph = np.triu(graph,1); graph += graph.T
        x = rng.normal(size=(6,3)); perm = np.array([3,0,5,1,4,2])
        for prefix,name,rows in [('d28','gcn_layer',3),('d29','graphsage_layer',6)]:
            f = load(prefix)[name]; weight = rng.normal(size=(rows,4))
            original = f(graph,x,weight)
            np.testing.assert_allclose(f(graph[np.ix_(perm,perm)],x[perm],weight),original[perm],atol=1e-12)
            self.assertTrue(np.all(original>=0))
        sage = load('d29')['graphsage_layer']
        weight = rng.normal(size=(6,4))
        np.testing.assert_allclose(sage(graph*7,x,weight),sage(graph,x,weight))

    def test_graph_readout_order_and_duplicate_nodes(self):
        f = load('d30')['graph_readout']
        rng = np.random.default_rng(530)
        x,batch = rng.normal(size=(9,3)),np.array([0,1,2,1,0,1,2,2,1])
        perm = rng.permutation(9)
        for mode in ['sum','mean','max']:
            baseline = f(x,batch,mode)
            np.testing.assert_allclose(f(x[perm],batch[perm],mode),baseline)
            duplicated = f(np.repeat(x,2,axis=0),np.repeat(batch,2),mode)
            np.testing.assert_allclose(duplicated,baseline*(2 if mode=='sum' else 1))

    def test_patch_layout_against_explicit_pixel_loops(self):
        f = load('d31')['patch_embeddings']
        rng = np.random.default_rng(531)
        images = rng.normal(size=(2,3,4,6)); weight = rng.normal(size=(5,12)); bias = rng.normal(size=5)
        expected = []
        for image in images:
            patches = []
            for row in range(0,4,2):
                for col in range(0,6,2):
                    flat = [image[c,row+i,col+j] for c in range(3) for i in range(2) for j in range(2)]
                    patches.append([sum(flat[k]*weight[d,k] for k in range(12))+bias[d] for d in range(5)])
            expected.append(patches)
        np.testing.assert_allclose(f(images,2,weight,bias),expected,atol=1e-12)
        identity = f(images,2,np.eye(12),np.zeros(12))
        np.testing.assert_allclose(identity.sum(axis=(1,2)),images.sum(axis=(1,2,3)))

    def test_noise_retention_matches_log_accumulation(self):
        f = load('d32')['linear_noise_schedule']
        result = f(1000,.0001,.02)
        expected = np.exp(np.cumsum(np.log1p(-result['betas'])))
        np.testing.assert_allclose(result['alpha_bar'],expected,rtol=1e-13)
        self.assertTrue(np.all(np.diff(result['alpha_bar'])<0))
        signal, noise = np.sqrt(result['alpha_bar']),np.sqrt(1-result['alpha_bar'])
        np.testing.assert_allclose(signal**2+noise**2,1)
        np.testing.assert_allclose(f(9,.5,.5)['alpha_bar'],.5**np.arange(1,10))

    def test_cached_attention_matches_full_pass_for_multiple_chunkings(self):
        f = load('e19')['cached_attention']
        rng = np.random.default_rng(519)
        q,k,v = rng.normal(size=(9,4)),rng.normal(size=(9,4)),rng.normal(size=(9,3))
        expected = []
        for i in range(9):
            scores = [sum(q[i,d]*k[j,d] for d in range(4))/2 for j in range(i+1)]
            weights = np.array([math.exp(score-max(scores)) for score in scores]); weights /= sum(weights)
            expected.append(weights@v[:i+1])
        np.testing.assert_allclose(f(q,k,v)['output'],expected,atol=1e-12)
        for sizes in [[1]*9,[2,4,3],[5,1,3]]:
            start,cache,outputs = 0,None,[]
            for size in sizes:
                stop = start+size
                result = f(q[start:stop],k[start:stop],v[start:stop],cache)
                cache = (result['keys'],result['values'])
                outputs.append(result['output']); start = stop
            np.testing.assert_allclose(np.concatenate(outputs),expected,atol=1e-12)
            np.testing.assert_array_equal(cache[0],k)
            np.testing.assert_array_equal(cache[1],v)
        changed = v.copy(); changed[4:] += 999
        np.testing.assert_array_equal(f(q,k,changed)['output'][:4],f(q,k,v)['output'][:4])

    def test_top_k_support_probability_ratios_and_shift_invariance(self):
        f = load('e20')['top_k_distribution']
        logits = np.array([2.,-1.,2.,.5,1.]); temperature = 1.7
        output = f(logits,3,temperature)
        np.testing.assert_array_equal(np.flatnonzero(output),[0,2,4])
        self.assertAlmostEqual(output.sum(),1)
        self.assertAlmostEqual(output[0]/output[4],math.exp((logits[0]-logits[4])/temperature))
        np.testing.assert_allclose(f(logits+1234,3,temperature),output)
        np.testing.assert_array_equal(f(np.ones(4),1),[1,0,0,0])

    def test_public_checks_reject_twelve_plausible_misconceptions(self):
        def wrong_swiglu(x,a,g,o):
            h,gate = np.asarray(x)@a,np.asarray(x)@g
            return (h/(1+np.exp(-gate)))@o

        def wrong_gcn(a,x,w):
            a = np.asarray(a)+np.eye(len(a))
            return np.maximum((a/a.sum(axis=1,keepdims=True))@x@w,0)

        def wrong_sage(a,x,w):
            x = np.asarray(x)
            out = np.maximum(np.concatenate([x,(np.asarray(a)>0)@x],axis=1)@w,0)
            return out/np.maximum(np.linalg.norm(out,axis=1,keepdims=True),1e-8)

        def wrong_patch(images,p,w,b):
            x = np.asarray(images); n,c,h,width = x.shape
            return x.reshape(n,-1,c*p*p)@np.asarray(w).T+b

        def wrong_cache(q,k,v,cache=None):
            q,k,v = np.asarray(q),np.asarray(k),np.asarray(v)
            if cache is not None:
                k,v = np.concatenate([cache[0],k]),np.concatenate([cache[1],v])
            scores = q@k.T/np.sqrt(k.shape[1]); weights = np.exp(scores-scores.max(axis=1,keepdims=True)); weights /= weights.sum(axis=1,keepdims=True)
            return {'output':weights@v,'keys':k,'values':v}

        def wrong_topk(logits,k,temperature=1):
            x = np.asarray(logits,dtype=float); keep = x>=np.sort(x)[-k]
            weights = np.where(keep,np.exp((x-x.max())/temperature),0)
            return weights/weights.sum()

        mistakes = {
            'd23':('gelu',lambda x:np.maximum(x,0)),
            'd24':('swiglu',wrong_swiglu),
            'd25':('batch_norm',lambda x,g,b,m,v,training=True,momentum=.1,eps=1e-5:load('d25')['batch_norm'](x,g,b,m,v,False,momentum,eps)),
            'd26':('label_smoothed_loss',lambda x,y,smoothing=.1:load('d26')['label_smoothed_loss'](x,y,smoothing*(np.asarray(x).shape[1]-1)/np.asarray(x).shape[1])),
            'd27':('contrastive_loss',lambda q,k,temperature=.07:load('d27')['contrastive_loss'](q,k,1)),
            'd28':('gcn_layer',wrong_gcn),
            'd29':('graphsage_layer',wrong_sage),
            'd30':('graph_readout',lambda x,b,mode='mean':np.maximum(load('d30')['graph_readout'](x,b,mode),0)),
            'd31':('patch_embeddings',wrong_patch),
            'd32':('linear_noise_schedule',lambda steps,beta_start=.0001,beta_end=.02:{'betas':np.linspace(beta_start,beta_end,steps),'alpha_bar':1-np.linspace(beta_start,beta_end,steps)}),
            'e19':('cached_attention',wrong_cache),
            'e20':('top_k_distribution',wrong_topk),
        }
        for prefix,(name,wrong) in mistakes.items():
            with self.subTest(activity=prefix),np.errstate(all='ignore'):
                results = load(prefix,'tests_public.py')['run_tests']({name:wrong})
                self.assertTrue(any(not row['passed'] and row['message'].startswith('AssertionError:') and not row['name'].startswith('Reject') for row in results),results)

    def test_provenance_notices_and_exact_source_links(self):
        manifest = json.loads((ROOT/'content/platform-batch-02-provenance.json').read_text(encoding='utf-8'))
        self.assertEqual(len(manifest['items']),12)
        self.assertEqual(sum(item['public_cases'] for item in manifest['items']),144)
        for item in manifest['items']:
            source = (BASE/item['folder']/'solution.py').read_text(encoding='utf-8')
            notice = (ROOT/item['notice']).read_text(encoding='utf-8')
            self.assertIn(manifest['revision'],item['upstream_url'])
            for value in ['Copyright (c) 2024 duoan','Copyright (c) 2024 kiren','Permission is hereby granted','THE SOFTWARE IS PROVIDED',item['upstream_url'],item['changes']]:
                self.assertIn(value,source)
                self.assertIn(value,notice)
            self.assertEqual(len(item['upstream_sha256']),64)


if __name__ == '__main__':
    unittest.main()

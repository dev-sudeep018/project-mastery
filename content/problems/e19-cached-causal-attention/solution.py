# Adapted from Pyre-Code / TorchCode. Source: https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/torch_judge/tasks/kv_cache.py
# Changes: Adapted the upstream cache concatenation and shifted causal mask. Removed learned projections, multiple heads and autograd so the cache state transition is directly inspectable. Original lesson prose and tests.
#
# MIT License
#
# This project is based on TorchCode by duoan (https://github.com/duoan/TorchCode),
# licensed under the MIT License.
#
# The `torch_judge/` package and `solutions/` notebooks are derived from the original project.
# The `web/` frontend and `grading_service/` backend are new additions.
#
# Copyright (c) 2024 duoan
# Copyright (c) 2024 kiren
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np

def _array(value):
    try:
        raw = np.asarray(value)
        if raw.dtype.kind not in "iuf":
            raise ValueError("Use real numeric arrays")
        result = raw.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Use real numeric arrays") from exc
    if not np.all(np.isfinite(result)) or np.any(np.abs(result) > 1e30):
        raise ValueError("Values must be finite with magnitude at most 1e30")
    return result

def _scalar(value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise ValueError("Use a real scalar")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("Scalar must be finite with magnitude at most 1e30") from exc
    if not np.isfinite(result) or abs(result) > 1e30:
        raise ValueError("Scalar must be finite with magnitude at most 1e30")
    return result

def _integer(value, low, high):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or not low <= value <= high:
        raise ValueError("Integer parameter outside the documented bounds")
    return int(value)


def cached_attention(queries, keys, values, cache=None):
    queries, keys, values = [_array(v) for v in (queries,keys,values)]
    if queries.ndim != 2 or keys.shape != queries.shape or any(n == 0 for n in queries.shape) or values.ndim != 2 or values.shape[0] != queries.shape[0] or values.shape[1] == 0:
        raise ValueError("Invalid new query, key or value shapes")
    if cache is None:
        past_keys, past_values = np.empty((0,keys.shape[1])),np.empty((0,values.shape[1]))
    else:
        if not isinstance(cache,tuple) or len(cache) != 2:
            raise ValueError("Cache must be a (keys,values) tuple")
        past_keys,past_values = [_array(v) for v in cache]
        if past_keys.ndim != 2 or past_values.ndim != 2 or past_keys.shape[0] != past_values.shape[0] or past_keys.shape[1] != keys.shape[1] or past_values.shape[1] != values.shape[1]:
            raise ValueError("Incompatible cache shapes")
    past = past_keys.shape[0]
    all_keys = np.concatenate([past_keys,keys],axis=0)
    all_values = np.concatenate([past_values,values],axis=0)
    scores = queries@all_keys.T/np.sqrt(keys.shape[1])
    allowed = np.arange(all_keys.shape[0])[None,:] <= past+np.arange(queries.shape[0])[:,None]
    scores = np.where(allowed,scores,-np.inf)
    exponentials = np.exp(scores-scores.max(axis=1,keepdims=True))
    probabilities = exponentials/exponentials.sum(axis=1,keepdims=True)
    return {"output":probabilities@all_values,"keys":all_keys,"values":all_values}

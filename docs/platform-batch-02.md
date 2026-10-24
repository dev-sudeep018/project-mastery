# Second licensed exercise-platform batch

Checked 24 October 2026. Twelve additional activities adapt selected operations
from the same pinned MIT-licensed Pyre-Code / TorchCode source as the pilot. They
add 144 public cases, bringing the catalog to 69 lessons plus one project
checkpoint and 854 public cases. The paths contain 17 mathematics/ML, 32 deep
learning and 20 engineering lessons. No fork duplicates or number-swapped variants
are counted.

## Learning objectives and adaptation choices

| ID  | Learning question                                               | Scope and conventions                                                                         |
| --- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| D23 | How does a Gaussian activation treat negative inputs?           | Exact erf GELU with Python math and NumPy; no gradient API                                    |
| D24 | What does a separate gate contribute to a projection?           | SwiGLU with a stable sigmoid and explicit matrix orientation                                  |
| D25 | Why must training and inference use different statistics?       | Returned state; population running variance explicitly differs from PyTorch's unbiased update |
| D26 | Where does label-smoothing probability mass go?                 | Non-target-only smoothing, including the zero/full-smoothing boundaries                       |
| D27 | How do in-batch negatives and temperature affect matched pairs? | One-directional InfoNCE; unit-vector validation; no symmetric CLIP/SimCLR claim               |
| D28 | How do node degrees affect incoming graph messages?             | Weighted undirected GCN with added self connections and symmetric normalization               |
| D29 | Why separate a node's own features from its neighbors?          | Full-neighborhood GraphSAGE mean aggregation; no random sampling; explicit norm floor         |
| D30 | What information does graph-level pooling preserve?             | Sum/mean/max readout with interleaved nodes and validated graph IDs                           |
| D31 | How does image layout become a token sequence?                  | Channel-first, row-major patches and a supplied affine projection                             |
| D32 | How does per-step noise compound over a schedule?               | Linear betas and cumulative alpha retention; no denoiser or quality claims                    |
| E19 | How does a cached prefix change the causal boundary?            | Single-head projected attention; cached and multi-token chunk correctness                     |
| E20 | Which tokens retain probability after top-k truncation?         | Deterministic distribution; exact-k index-order ties; no random draw or top-p filtering       |

Each activity has original teaching prose, three worked examples, hints, a starter,
an attributed reference and twelve public cases. Prerequisites connect the graph
lessons, attention/cache lessons and existing foundation material. These are
learning operations on small supplied arrays, not complete model-training systems.

The general engineering lesson link now invites learners to explore the retrieval
project without implying that the project implements every engineering topic,
including KV caching and token sampling.

## Source record

[The provenance manifest](../content/platform-batch-02-provenance.json) pins
commit `7ede95b47437798c74023a0ffae8fb33bbeebc2e`, twelve source-file hashes and the
license hash. Full MIT notices for duoan and kiren remain in each package's
`THIRD_PARTY_NOTICE.md` and `solution.py`, including the browser-delivered reference.
Original additions are Apache-2.0 and original prose is CC BY-SA 4.0; the upstream
material retains MIT terms. See the [pinned license](https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/LICENSE).

The BatchNorm variance distinction was checked against the
[PyTorch BatchNorm1d documentation](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm1d.html).

Only source text was read. Upstream programs, installers and test code were not
executed. Selected solution equations were ported to the existing NumPy runtime;
the task descriptions and fixtures here are original. The pilot's TensorTonic,
Deep-ML and HappyTorch decisions remain unchanged.

## Verification strategy

The batch check executes all references, starters, samples and a trivial wrong
answer. Thirteen additional Python methods check independent scalar/loop oracles,
GELU derivatives, normalization state transitions, loss invariances, graph
permutation/duplication behavior, patch order, cumulative retention, cached/full
attention equivalence and decoding probabilities. Every public evaluator rejects
a plausible conceptual mistake on valid input. Those mistakes include future-token
leakage, a row-only graph normalization and retaining too many tied top-k tokens.

Run `pnpm content:check d23 d24 d25 d26 d27 d28 d29 d30 d31 d32 e19 e20`, then
`pnpm check`. The existing browser suite discovers each new reference automatically.
[The verification record](verification.md) distinguishes executed results from the
remaining physical-device and learner-review limitations.

# Adapting exercise platforms

Checked 23 October 2026. Following the request to use platforms such as
TensorTonic, this pilot adds six activities adapted from Pyre-Code's MIT-licensed
task implementations. The catalog now has 57 lessons plus one project checkpoint,
with 710 public cases. Paths contain 17 mathematics/ML, 22 deep-learning and 18
engineering lessons. External catalog sizes and framework variants do not count
as additional published activities.

## Platform decisions

| Platform                                                   | Evidence inspected                                                                                                                                                                                | Use here                                                                                 |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [TensorTonic](https://www.tensortonic.com)                 | [Terms](https://www.tensortonic.com/terms) prohibit copying, scraping, derivatives and redistribution                                                                                             | External reference; no problem statements, solutions or tests imported                   |
| [Deep-ML](https://github.com/Open-Deep-ML/DML-OpenProblem) | [Pinned license](https://github.com/Open-Deep-ML/DML-OpenProblem/blob/04708b485a051316c25b91e4cb9a2ada0ccf7fbf/LICENSE) permits educational use with commercial-use and sublicensing restrictions | External reference pending a compatible grant; do not relabel as Apache-2.0 or CC BY-SA  |
| [Pyre-Code](https://github.com/whwangovo/pyre-code)        | [Pinned MIT license](https://github.com/whwangovo/pyre-code/blob/7ede95b47437798c74023a0ffae8fb33bbeebc2e/LICENSE), selected task files and TorchCode lineage                                     | Six NumPy adaptations; both upstream copyright notices retained                          |
| [HappyTorch](https://github.com/Rivflyyy/HappyTorch)       | [Pinned MIT license](https://github.com/Rivflyyy/HappyTorch/blob/603c33e397dbd0893d222210e3fe6bd6bc514efd/LICENSE) and TorchCode lineage                                                          | Additional candidate source; inspect files and deduplicate shared ancestry before import |

The [registry](../content/sources.json) contains 25 inspected resources. These are
editorial decisions for this project's licensing model, not blanket permission
to republish every free exercise platform.

## The six adaptations

| ID  | Activity and learning question                                     | Changes                                                                                                                          |
| --- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| D18 | RMS normalization: what changes without mean subtraction?          | NumPy forward equation, explicit shape/epsilon rules                                                                             |
| D19 | RoPE: how can rotation preserve norms and encode relative offsets? | Adjacent-pair NumPy rotation, deterministic invariance cases                                                                     |
| D20 | LoRA: how does a low-rank update change a fixed mapping?           | Supplied-array forward function replacing a trainable class; no autograd claims                                                  |
| D21 | Cosine schedule: where do warmup and decay meet?                   | Scalar schedule retained; interval/rate validation added                                                                         |
| D22 | Focal loss: how are easy-example contributions reduced?            | Stable log-softmax replaces probability-plus-epsilon, avoiding an artificial loss cap                                            |
| E18 | INT8 weights: what error does each channel's scale introduce?      | Explicit zero-row scale, symmetric [-127,127], ties-to-even rounding, inspectable storage/output and documented numerical bounds |

Each package includes three worked examples, hints, starter code, a reference,
original public tests and a path connection. The six add 73 public cases. No
PyTorch, model service, paid API or external dataset is needed. A NumPy forward
pass is explicitly distinguished from the upstream training task.

## Provenance and repeatability

[The manifest](../content/platform-pilot-provenance.json) pins the source commit,
task paths, SHA-256 hashes, changes and notice locations. Full upstream MIT notices
remain in each reference, so credits travel to the browser solution view, and in
each `THIRD_PARTY_NOTICE.md`. Original additions are Apache-2.0; original prose is
CC BY-SA 4.0; upstream material retains MIT terms.

Upstream programs and setup scripts were not executed. Selected numerical
operations were read and ported; prose and fixtures were authored for our
contracts. Retrieve the pinned source files and compare their manifest hashes to
reproduce the source snapshot.

For future batches, compare objectives against the catalog, inspect exact file
licenses/notices, port the required operation, and add independent numerical and
misconception checks. Deduplicate forks. Keep framework-specific training tasks
for a runtime that can execute them.

Run `pnpm content:check d18 d19 d20 d21 d22 e18`, then `pnpm check`. Eight new Python
methods check RMS energy, RoPE common-shift dot products, LoRA merged weights,
quantization error, schedule monotonicity, focal-loss shift invariance, six
plausible wrong implementations and retained notices. Browser reference tests
discover the six packages automatically. See [verification.md](verification.md)
for executed results and limitations.

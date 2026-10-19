# Contributing

Use a short-lived branch and a focused pull request. Describe the learner-visible outcome, the checks you ran, and any verification limits. Do not add credentials, uploaded learner code, generated runtime files, or node_modules.

## Getting started

Follow README.md, then run `pnpm check` and the relevant browser tests. The lockfile and Python runtime are pinned. `pnpm setup` prepares generated content and locally served third-party runtime files.

## Adding an exercise

Create a directory under content/problems containing problem.yaml, explanation.md, starter.py, solution.py, and tests_public.py. Follow the existing schema. `run_tests(namespace, mode)` must return named results with passed and message fields.

The schema validator checks unique IDs, unique slugs, required files, prerequisite existence, cycles, and supported packages. Python validation executes reference solutions against the same evaluator used in the browser. Include tests that reject plausible wrong implementations. Do not publish copied proprietary explanations or unlicensed datasets.

The first runner supports only m02/v1. Supporting another exercise requires explicitly extending the versioned runner contract and adding browser tests. Metadata alone cannot silently introduce executable content.

## Review

All contributions need maintainer review. CI does not substitute for mathematical review or a security audit. A validated content status means automated checks passed, not independent expert endorsement.

Original software contributions are licensed under Apache-2.0. Original educational prose is licensed under CC BY-SA 4.0. Keep third-party attribution and license notices. By contributing, you confirm you have the right to contribute your work under these terms.

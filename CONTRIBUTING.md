# Contributing

Use a short-lived branch and a focused pull request. Describe the learner-visible outcome, the checks you ran, and any verification limits. Do not add credentials, uploaded learner code, generated runtime files, or node_modules.

## Getting started

Follow README.md, then run `pnpm check` and the relevant browser tests. The lockfile and Python runtime are pinned. `pnpm setup` prepares generated content and locally served third-party runtime files.

## Adding an exercise

Create a directory under content/problems containing problem.yaml, lesson.json, explanation.md, starter.py, solution.py, and tests_public.py. Follow the existing schema and [curriculum requirements](docs/curriculum.md). Start with status `draft`. `run_tests(namespace, mode)` must return named results with passed and message fields. The shared helpers in `content/evaluator_helpers.py` are prepended in both native Python checks and browser evaluators.

The schema validator checks unique IDs, unique slugs, required files, prerequisite existence, cycles, and supported packages. Python validation executes reference solutions against the same evaluator used in the browser. Include tests that reject plausible wrong implementations. Do not publish copied proprietary explanations or unlicensed datasets.

After automated validation and review, a validated package enters the generated versioned runner allowlist. Drafts do not appear in the application. Browser regression tests discover each published package and execute its reference. `lesson.json` declares the exact full test count; sample mode must run three cases. Changing a published grading contract requires a new version.

## Review

All contributions need maintainer review. CI does not substitute for mathematical review or a security audit. A validated content status means automated checks passed, not independent expert endorsement.

Original software contributions are licensed under Apache-2.0. Original educational prose is licensed under CC BY-SA 4.0. Keep third-party attribution and license notices. By contributing, you confirm you have the right to contribute your work under these terms.
